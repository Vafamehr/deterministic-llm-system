from typing import Dict, Any

from agent_decision import AgentDecision
from agent_action import AgentAction


class AgentController:
    def __init__(self, max_steps: int = 1):
        self.max_steps = max_steps

    def decide(
        self,
        goal: str,
        step_index: int,
        stage_results: Dict[str, Dict[str, Any]],
    ) -> AgentDecision:

        # Hard boundary
        if step_index >= self.max_steps:
            return AgentDecision(
                action=AgentAction.STOP,
                reason="Max step limit reached",
                step_index=step_index,
            )

        det_result = stage_results.get("deterministic")

        if det_result and det_result.get("status") != "success":
            return AgentDecision(
                action=AgentAction.RUN_LLM,
                reason="Deterministic stage did not succeed; request LLM fallback",
                step_index=step_index,
            )

        return AgentDecision(
            action=AgentAction.STOP,
            reason="No additional action required",
            step_index=step_index,
        )