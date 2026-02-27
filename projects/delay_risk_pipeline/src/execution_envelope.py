from dataclasses import dataclass
from typing import Set
from enum import Enum


class AllowedAction(str, Enum):
    RUN_LLM = "run_llm"
    STOP = "stop"

""" 
Why frozen=True?
This makes the dataclass immutable.

Meaning:

Once created, it cannot be modified.

Governance defines it.

Agent cannot mutate it.

That's intentional.

"""
@dataclass(frozen=True)
class ExecutionEnvelope:
    """
    Defines which actions the agent is permitted to take
    for the current pipeline execution.
    """

    allowed_actions: Set[AllowedAction]
    reason: str  # short explanation for logging/trace

    def allows(self, action: AllowedAction) -> bool:
        return action in self.allowed_actions