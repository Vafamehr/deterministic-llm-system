from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ToolSpec:
    """
    Immutable definition of a tool.

    - name: unique identifier
    - description: what it does
    - input_schema: expected keys/types (lightweight for now)
    - output_schema: expected result structure
    """
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


@dataclass
class ToolRequest:
    """
    A request to execute a tool.

    Created by orchestrator (not agent).
    """
    tool_name: str
    arguments: Dict[str, Any]


@dataclass
class ToolResult:
    """
    Result of executing a tool.

    - success: whether execution succeeded
    - data: returned payload (if success)
    - error: error message (if failure)
    """
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None