from typing import Dict, Any, Optional

from agent_decision import AgentDecision
from agent_action import AgentAction
from execution_envelope import ExecutionEnvelope, AllowedAction

class AgentController:
    def __init__(self):
        # self.max_steps = max_steps removed agent don have control on this anymore. Day 33. instead step budget
        pass

    def decide(
        self,
        goal: str,
        step_index: int,
        step_budget: int,  # NEW: provided by orchestrator
        stage_results: Dict[str, Dict[str, Any]],
        trace_context: Optional[Dict[str, Any]] = None,
        governance_context: Optional[Dict[str, Any]] = None,
        envelope: Optional[ExecutionEnvelope] = None,
        delta_context: Optional[Dict[str, Any]] = None,  # Day 
    ) -> AgentDecision:
        

        trace_context = trace_context or {}
        governance_context = governance_context or {}
        delta_context = delta_context or {}
        if step_index == 1:
            if "proposed_action" not in delta_context:
                return AgentDecision(
                    action=AgentAction.STOP,
                    reason="step_1_requires_delta_context_for_confirmation",
                    requested_by="orchestrator_guardrail",
                    step_index=step_index,
                )
        # If no envelope provided, allow current behavior (temporary default)
        if envelope is None:
            raise ValueError("ExecutionEnvelope must be provided by the pipeline")
            
        def _enforce(action: AgentAction, reason: str) -> AgentDecision:
            desired = AllowedAction.RUN_LLM if action == AgentAction.RUN_LLM else AllowedAction.STOP

            if envelope.allows(desired):
                return AgentDecision(
                    action=action,
                    reason=reason,
                    step_index=step_index,
                    requested_by="agent_controller",
                )

            # If blocked, fallback to STOP only if STOP is allowed
            blocked_reason = (
                f"Envelope blocked '{desired.value}'. Attempting fallback to 'stop'. "
                f"Envelope reason: {envelope.reason}"
            )

            if envelope.allows(AllowedAction.STOP):
                return AgentDecision(
                    action=AgentAction.STOP,
                    reason=blocked_reason,
                    step_index=step_index,
                    requested_by="agent_controller",
                )

            # If even STOP is not allowed, fail closed with a hard error
            # (This should never happen if envelopes are built correctly.)
            raise ValueError(
                f"Invalid envelope: neither '{desired.value}' nor 'stop' allowed. "
                f"Allowed: {[a.value for a in envelope.allowed_actions]}"
            )   
          
        # Hard boundary
        if step_index >= step_budget:
            return AgentDecision(
                            action=AgentAction.STOP,
                            reason=f"Step budget exhausted ({step_budget})"
                            )

        llm_attempted = trace_context.get("llm_attempted", False)
        hard_stop = governance_context.get("hard_stop", False)
        needs_review = governance_context.get("needs_review", False)

        # Governance can forbid any follow-up
        if hard_stop:
            return _enforce(AgentAction.STOP, "Governance hard_stop=True")

        det_result = stage_results.get("deterministic") or {}
        det_status = (det_result.get("status") or "").lower()

        # Rule 1 (existing): deterministic failure → try LLM once
        if det_status and det_status != "success" and not llm_attempted:
            return _enforce(
                AgentAction.RUN_LLM,
                "Deterministic stage did not succeed; request LLM fallback",
            )

        # Rule 2 (new): governance says output is risky → try LLM once (if not already)
        if needs_review and not llm_attempted:
            return _enforce(
                AgentAction.RUN_LLM,
                "Governance flagged needs_review; request one LLM follow-up for safer assessment",
            )

        # Otherwise, stop (bounded + conservative)
        return _enforce(AgentAction.STOP, "No additional action required")