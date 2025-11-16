# Azure AI Travel Assistant with Redis Knowledge Store

This demo showcases an Azure AI Foundry agent that uses a Redis MCP (Model Context Protocol) server to access travel destination data stored in Azure Managed Redis with vector search capabilities.

## Overview

The demo consists of two main components:

1. **Knowledge Store Setup** (`create_knowledge_store.py`) - Creates and populates a vector store in Azure Managed Redis with travel destination data
2. **Travel Assistant Agent** (`travel_assistant_agent.py`) - Creates an Azure AI Foundry agent that can query a knowledge store in Azure Managed Redis via MCP tools

## Prerequisites

- Azure Foundry project. For more information, see [How to create Azure Foundry project](https://learn.microsoft.com/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry)
- Azure Found model. For more information, see [How to deploy model](https://learn.microsoft.com/azure/ai-foundry/foundry-models/how-to/create-model-deployments?pivots=ai-foundry-portal)
- Azure Managed Redis remote MCP server. For more information, see [how to install a remote Azure Managed Redis server](https://github.com/AzureManagedRedis/mcp-amr?tab=readme-ov-file#installation)

## Setup

### 1. Environment Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Update the `.env` file with your actual values.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Azure Authentication

Ensure you're authenticated to Azure:

```bash
az login
```

## Usage

### Step 1: Create and Populate Knowledge Store

Run the knowledge store creation script to set up the Redis vector store with travel destination data:

```bash
python create_knowledge_store.py
```

This script will:
- Connect to the Redis MCP server
- Create a knowledge store named "destinations"
- Populate it with detailed travel destination information
- Verify the data was stored correctly

### Step 2: Run the Travel Assistant Agent

Start the interactive travel assistant:

```bash
python travel_assistant_agent.py
```

The agent will:
- Create an Azure AI Foundry agent with MCP tools
- Connect to the Redis knowledge store
- Allow you to query for travel recommendations

### Example Queries

Try asking the agent questions like:
- "I am Alice. I like food tours and travel with kids. Recommend me beach destinations."
- "I'm looking for a family-friendly destination with beautiful nature"
- "Recommend a place for hiking and outdoor adventures"
- "What's a good tropical destination for relaxation?"
- "Show me destinations with rich cultural experiences"

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MCP_SERVER_URL` | Redis MCP server endpoint | `https://redis-mcp-app.azurecontainerapps.io/message` |
| `MCP_SERVER_SSE_URL` | Redis MCP server endpoint | `https://redis-mcp-app.azurecontainerapps.io/sse` |
| `MCP_API_KEY` | API key for Redis MCP server | `your-api-key-here` |
| `PROJECT_ENDPOINT` | Azure AI Foundry project endpoint | `https://your-project.services.ai.azure.com/api/projects/your-project` |
| `MODEL_NAME` | AI model deployment name | `gpt-4o` |

### Redis MCP Server

This demo requires a Redis MCP server that provides:
- `knowledge_store_put` - Store data in Redis knowledge store
- `knowledge_store_search` - Semantic search in knowledge store
- Vector similarity search capabilities