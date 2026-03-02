from typing import Callable, Dict

from tools.contracts import ToolRequest, ToolResult
from tools.envelope import ToolEnvelope


class ToolRunner:
    """
    Deterministic executor for tools.

    - Does NOT decide which tool to run.
    - Executes exactly what orchestrator requested.
    - Enforces ToolEnvelope permissions + max_calls.
    """

    def __init__(self, registry: Dict[str, Callable]):
        # registry: tool_name -> callable
        self._registry = registry

    def run(self, request: ToolRequest, envelope: ToolEnvelope) -> ToolResult:
        # Permission check (allow-list)
        if not envelope.allows(request.tool_name):
            return ToolResult(
                success=False,
                error=f"Tool '{request.tool_name}' not allowed by envelope",
            )

        # Registration check (tool must exist)
        if request.tool_name not in self._registry:
            return ToolResult(
                success=False,
                error=f"Tool '{request.tool_name}' not registered",
            )

        try:
            # Enforce max_calls to prevent loops/retries
            envelope.record_call()

            tool_fn = self._registry[request.tool_name]
            result = tool_fn(**request.arguments)  # tool returns Dict[str, Any]

            return ToolResult(success=True, data=result)

        except Exception as e:
            return ToolResult(success=False, error=str(e))