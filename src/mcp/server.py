from mcp.server.fastapi import MCPFastAPI

from src.mcp.tools.preocr_tool import preocr_tool
from src.mcp.tools.ingest_tool import ingest_tool
from src.mcp.tools.vector_search_tool import vector_search_tool

mcp_app = MCPFastAPI(
    title="Agentic RAG MCP Server",
    description="MCP tools for Agentic RAG system",
)

# Register tools
mcp_app.add_tool(preocr_tool)
mcp_app.add_tool(ingest_tool)
mcp_app.add_tool(vector_search_tool)
