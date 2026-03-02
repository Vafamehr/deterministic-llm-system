from dataclasses import dataclass, field
from typing import Set


@dataclass
class ToolEnvelope:
    """
    Governs which tools are allowed to execute during this pipeline run.

    The orchestrator creates this.
    The agent never modifies it.
    """

    allowed_tools: Set[str] = field(default_factory=set)
    max_calls: int = 1  # keep deterministic — no loops

    _calls_made: int = field(default=0, init=False, repr=False)

    def allows(self, tool_name: str) -> bool:
        """
        Check whether a tool is permitted.
        """
        return tool_name in self.allowed_tools

    def record_call(self) -> None:
        """
        Track that a tool execution occurred.
        Enforces max_calls constraint.
        """
        self._calls_made += 1
        if self._calls_made > self.max_calls:
            raise RuntimeError(
                f"ToolEnvelope exceeded max_calls={self.max_calls}"
            )

    @property
    def calls_made(self) -> int:
        return self._calls_made