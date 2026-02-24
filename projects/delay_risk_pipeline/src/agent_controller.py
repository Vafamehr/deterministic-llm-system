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
        trace_context: Optional[Dict[str, Any]] = None, # trace aware from day 31
        governance_context: Optional[Dict[str, Any]] = None,  # Day 32: governance-aware
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
        governance_context = governance_context or {}

        llm_attempted = trace_context.get("llm_attempted", False)

        hard_stop = governance_context.get("hard_stop", False)
        needs_review = governance_context.get("needs_review", False)

        # Governance can forbid any follow-up
        if hard_stop:
            return AgentDecision(
                action=AgentAction.STOP,
                reason="Governance hard stop enabled; no follow-up allowed",
                step_index=step_index,
                requested_by="agent_controller",
            )

        det_result = stage_results.get("deterministic") or {}
        det_status = (det_result.get("status") or "").lower()

        # Rule 1 (existing): deterministic failure → try LLM once
        if det_status and det_status != "success" and not llm_attempted:
            return AgentDecision(
                action=AgentAction.RUN_LLM,
                reason="Deterministic stage did not succeed; request LLM fallback",
                step_index=step_index,
                requested_by="agent_controller",
            )

        # Rule 2 (new): governance says output is risky → try LLM once (if not already)
        if needs_review and not llm_attempted:
            return AgentDecision(
                action=AgentAction.RUN_LLM,
                reason="Governance flagged needs_review; request one LLM follow-up for safer assessment",
                step_index=step_index,
                requested_by="agent_controller",
            )

        # Otherwise, stop (bounded + conservative)
        return AgentDecision(
            action=AgentAction.STOP,
            reason="No additional action required",
            step_index=step_index,
            requested_by="agent_controller",
        )