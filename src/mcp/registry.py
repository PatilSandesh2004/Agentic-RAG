from src.mcp.tools.preocr_tool import preocr_tool
from src.mcp.tools.ingest_tool import ingest_tool
from src.mcp.tools.vector_search_tool import vector_search_tool


MCP_TOOLS = {
    "preocr.check_document": preocr_tool,
    "documents.ingest": ingest_tool,
    "vector.search": vector_search_tool,
}
