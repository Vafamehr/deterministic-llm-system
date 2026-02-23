"""
Docstring for projects.delay_risk_pipeline.src.agent_decision

Structured, explicit decision control.
"""




from dataclasses import dataclass
from typing import Optional

from agent_action import AgentAction


@dataclass
class AgentDecision:
    action: AgentAction
    reason: str
    requested_by: str = "agent"
    step_index: Optional[int] = None