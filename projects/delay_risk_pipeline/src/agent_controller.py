from typing import Dict, Any, Optional

from agent_decision import AgentDecision
from agent_action import AgentAction
from execution_envelope import ExecutionEnvelope, AllowedAction




class AgentController:
    """
    AgentController = bounded evaluator (NOT autonomous).

    Days 33-35 invariants:
    - Orchestrator owns sequencing and authority.
    - Agent does not loop/extend itself. No recursion.
    - step_budget is provided by orchestrator (agent has no control over #passes).
    - ExecutionEnvelope is mandatory and is the hard action boundary.
    - Step 1 (if scheduled) is a CONFIRMATION pass using delta_context, not a retry.
      * Monotonic: can hold or downgrade, never upgrade.
      * Downgrade must cite a concrete constraint from delta_context.
    """

    def __init__(self):
        # Day 33: removed agent-owned step control (e.g., max_steps).
        # Orchestrator now controls pass count via step_budget.
        pass

    def decide(
        self,
        goal: str,
        step_index: int,
        step_budget: int,  # Day 33: provided by orchestrator
        stage_results: Dict[str, Dict[str, Any]],
        trace_context: Optional[Dict[str, Any]] = None,
        governance_context: Optional[Dict[str, Any]] = None,
        envelope: Optional[ExecutionEnvelope] = None,
        delta_context: Optional[Dict[str, Any]] = None,  # Day 34: Step0→Step1 delta
    ) -> AgentDecision:

        trace_context = trace_context or {}
        governance_context = governance_context or {}
        delta_context = delta_context or {}

        # Envelope is mandatory: no action without an explicit boundary.
        if envelope is None:
            raise ValueError("ExecutionEnvelope must be provided by the pipeline")

        def _enforce(action: AgentAction, reason: str) -> AgentDecision:
            """
            Enforce the ExecutionEnvelope boundary.

            - If desired action is allowed → return it.
            - If blocked → attempt conservative fallback to STOP (if allowed).
            - If STOP also blocked → fail closed (hard error).
            """
            desired = AllowedAction.RUN_LLM if action == AgentAction.RUN_LLM else AllowedAction.STOP

            if envelope.allows(desired):
                return AgentDecision(
                    action=action,
                    reason=reason,
                    step_index=step_index,
                    requested_by="agent_controller",
                )

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

            raise ValueError(
                f"Invalid envelope: neither '{desired.value}' nor 'stop' allowed. "
                f"Allowed: {[a.value for a in envelope.allowed_actions]}"
            )

        # Day 33: hard boundary. If orchestrator calls beyond budget, fail closed.
        if step_index >= step_budget:
            return AgentDecision(
                action=AgentAction.STOP,
                reason=f"Step budget exhausted ({step_budget})",
                step_index=step_index,
                requested_by="agent_controller",
            )

        # ----------------------------
        # Day 34–35: Step 1 confirmation mode (delta-based, not retry)
        # ----------------------------
        if step_index == 1:
            # Day 34 guardrail: Step 1 MUST receive delta_context (prevents silent retry).
            if "proposed_action" not in delta_context:
                return AgentDecision(
                    action=AgentAction.STOP,
                    reason="step_1_requires_delta_context_for_confirmation",
                    requested_by="orchestrator_guardrail",
                    step_index=step_index,
                )

            prior_action = delta_context.get("proposed_action")  # string: "run_llm" or "stop"

            # Day 35 monotonicity: Step 1 cannot "upgrade".
            # If Step 0 proposed STOP, Step 1 must remain STOP.
            if prior_action == AgentAction.STOP.value:
                return AgentDecision(
                    action=AgentAction.STOP,
                    reason="confirmation_pass: prior_action_stop_enforced",
                    requested_by="orchestrator_confirmation_policy",
                    step_index=step_index,
                )

            # Day 35 constraint-cited downgrade:
            # If Step 0 proposed RUN_LLM, Step 1 may downgrade ONLY if a concrete
            # constraint in delta_context indicates we must stop.
            if prior_action == AgentAction.RUN_LLM.value:
                known = delta_context.get("known_constraints") or {}

                # Concrete constraint: governance hard_stop captured in delta.
                if known.get("hard_stop", False):
                    return _enforce(AgentAction.STOP, "confirmation_pass: hard_stop_in_delta")

                # Concrete constraint: envelope disallows RUN_LLM captured in delta.
                allowed = set(known.get("allowed_actions") or [])
                if AllowedAction.RUN_LLM.value not in allowed:
                    return _enforce(AgentAction.STOP, "confirmation_pass: envelope_disallows_run_llm")

                # Otherwise confirm Step 0's RUN_LLM proposal.
                # IMPORTANT: Step 1 does NOT re-run Rule 1 / Rule 2 logic.
                return _enforce(AgentAction.RUN_LLM, "confirmation_pass: constraints_ok_confirm_run_llm")

            # Unknown prior action → fail closed.
            return _enforce(AgentAction.STOP, "confirmation_pass: unknown_prior_action_fail_closed")

        # ----------------------------
        # Step 0 policy (bounded evaluator)
        # ----------------------------
        llm_attempted = trace_context.get("llm_attempted", False)
        hard_stop = governance_context.get("hard_stop", False)
        needs_review = governance_context.get("needs_review", False)

        # Governance can forbid any follow-up.
        if hard_stop:
            return _enforce(AgentAction.STOP, "Governance hard_stop=True")

        det_result = stage_results.get("deterministic") or {}
        det_status = (det_result.get("status") or "").lower()

        # Rule 1: deterministic failure → request LLM once (if not already attempted).
        if det_status and det_status != "success" and not llm_attempted:
            return _enforce(
                AgentAction.RUN_LLM,
                "Deterministic stage did not succeed; request LLM fallback",
            )

        # Rule 2: governance says output is risky → request one LLM follow-up (if not already attempted).
        if needs_review and not llm_attempted:
            return _enforce(
                AgentAction.RUN_LLM,
                "Governance flagged needs_review; request one LLM follow-up for safer assessment",
            )

        # Otherwise STOP (bounded + conservative).
        return _enforce(AgentAction.STOP, "No additional action required")