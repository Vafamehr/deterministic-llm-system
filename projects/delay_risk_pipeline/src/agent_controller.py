from typing import Dict, Any, Optional

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
        trace_context: Optional[Dict[str, Any]] = None,  # Day 31: trace-aware
    ) -> AgentDecision:

        # Hard boundary
        if step_index >= self.max_steps:
            return AgentDecision(
                action=AgentAction.STOP,
                reason="Max step limit reached",
                step_index=step_index,
                requested_by="agent_controller",
            )

        trace_context = trace_context or {}
        steps_run = trace_context.get("steps_run", [])
        llm_attempted = trace_context.get("llm_attempted", False)

        det_result = stage_results.get("deterministic") or {}
        det_status = (det_result.get("status") or "").lower()

        # If deterministic failed and we haven't tried LLM yet, request one follow-up LLM run.
        if det_status and det_status != "success" and not llm_attempted:
            return AgentDecision(
                action=AgentAction.RUN_LLM,
                reason="Deterministic stage did not succeed; request LLM fallback",
                step_index=step_index,
                requested_by="agent_controller",
            )

        # If LLM already happened (or deterministic is fine), stop.
        # We keep this conservative and bounded.
        return AgentDecision(
            action=AgentAction.STOP,
            reason="No additional action required",
            step_index=step_index,
            requested_by="agent_controller",
        )