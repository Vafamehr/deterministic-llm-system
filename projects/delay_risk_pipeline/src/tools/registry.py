from tools.basic_tools import get_current_time
from .retrieval import  rag_retrieve

# Central registry: tool_name -> callable

TOOL_REGISTRY = {
    "get_current_time": get_current_time,
    "rag.retrieve": rag_retrieve,
}