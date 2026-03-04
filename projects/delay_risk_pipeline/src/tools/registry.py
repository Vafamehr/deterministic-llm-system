from tools.basic_tools import get_current_time
from .retrieval import RETRIEVAL_TOOL

# Central registry: tool_name -> callable
TOOL_REGISTRY = {
    "get_current_time": get_current_time,
    RETRIEVAL_TOOL.name: RETRIEVAL_TOOL,
}