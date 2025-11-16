import os
import time
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import (
    ListSortOrder,
    McpTool,
    RequiredMcpToolCall,
    SubmitToolApprovalAction,
    ToolApproval,
)

load_dotenv()

# Load configuration from environment variables
mcp_server_url = os.environ.get("MCP_SERVER_URL")
mcp_server_label = os.environ.get("MCP_SERVER_LABEL", "redis")
mcp_api_key = os.environ.get("MCP_API_KEY")
project_endpoint = os.environ.get("PROJECT_ENDPOINT")
model_name = os.environ.get("MODEL_NAME", "gpt-4o")

# Validate required environment variables
if not all([mcp_server_url, project_endpoint, mcp_api_key]):
    raise ValueError(
        "Missing required environment variables. Please set: "
        "MCP_SERVER_URL, PROJECT_ENDPOINT, MCP_API_KEY in .env file"
    )

print(f"Using MCP Server: {mcp_server_url}")
print(f"Using Project Endpoint: {project_endpoint}")
print(f"Using Model: {model_name}")

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

mcp_tool = McpTool(
    server_label=mcp_server_label,
    server_url=mcp_server_url,
    allowed_tools=[],
)
mcp_tool.update_headers("x-api-key", mcp_api_key)

def run_agent_message(agents_client, agent, thread, message_content):
    message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_content,
    )
    run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id, tool_resources=mcp_tool.resources)
    while run.status in ["queued", "in_progress", "requires_action"]:
        time.sleep(1)
        run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
        if run.status == "requires_action" and isinstance(run.required_action, SubmitToolApprovalAction):
            tool_calls = run.required_action.submit_tool_approval.tool_calls
            if not tool_calls:
                agents_client.runs.cancel(thread_id=thread.id, run_id=run.id)
                break
            tool_approvals = []
            for tool_call in tool_calls:
                if isinstance(tool_call, RequiredMcpToolCall):
                    tool_approvals.append(
                        ToolApproval(
                            tool_call_id=tool_call.id,
                            approve=True,
                            headers=mcp_tool.headers,
                        )
                    )
            if tool_approvals:
                agents_client.runs.submit_tool_outputs(
                    thread_id=thread.id, run_id=run.id, tool_approvals=tool_approvals
                )

    # Fetch and log all messages
    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    print("\nConversation:")
    print("-" * 50)
    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role.upper()}: {last_text.text.value}")
            print("-" * 50)

def main():
    with project_client:
        agents_client = project_client.agents
        agent = agents_client.create_agent(
            model=model_name,
            name="travel-assistant",
            instructions="You are a travel destination recommender."
            "Always store and search for user preferences in Redis MCP tool. Preferences are stored as username_preferences, all lowercase."
            "Always recommend destinations included in destinations knowledge store from Redis MCP tool only.",
            tools=mcp_tool.definitions,
        )
        print(f"Created agent: {agent.id}")
        
        thread = agents_client.threads.create()
        print(f"Created thread: {thread.id}")
        print("\nType your query. Type 'exit' to quit.")
        
        while True:
            message = input("Query>> ")
            if message.strip().lower() == "exit":
                break
            run_agent_message(agents_client, agent, thread, message)
        
        agents_client.delete_agent(agent.id)
        print("Deleted agent")

if __name__ == "__main__":
    main()