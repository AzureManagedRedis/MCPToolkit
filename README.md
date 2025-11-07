# MCPToolkit

This repository serves as a central hub for all MCP (Model Context Protocol) related resources for Azure Managed Redis (AMR). 

## Azure Managed Redis MCP server

Following is a list of recommended MCP servers (local or self-hosted remote) for using Azure Managed Redis.

1. [mcp-amr](https://github.com/AzureManagedRedis/mcp-amr): This MCP server is a natural languange interface for querying and accessing data in your Azure Managed Redis instances. It offers the 'knowledge store' set of tools which simplifies performing vector search/RAG operations on Azure Managed Redis. It is a fork of mcp-redis and can be self-hosted remote in Azure using detailed instructed in the repo.
   
1. [mcp-redis](https://github.com/redis/mcp-redis): This is the official Redis MCP server, designed for agentic applications to efficiently manage and search data in Redis.
   
1. [Azure MCP Server](https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server): This MCP server for Azure services supports management operations for your Azure Managed Redis instances.
