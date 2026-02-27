from typing import Dict, Any
from execution_envelope import ExecutionEnvelope, AllowedAction


def build_execution_envelope(governance: Dict[str, Any]) -> ExecutionEnvelope:
    """
    Convert governance outputs into a hard action boundary for the agent.
    Only two actions exist in this repo right now: RUN_LLM or STOP.
    """

    hard_stop = bool(governance.get("hard_stop", False))
    needs_review = bool(governance.get("needs_review", False))

    # If hard stop: only STOP is allowed.
    if hard_stop:
        return ExecutionEnvelope(
            allowed_actions={AllowedAction.STOP},
            reason="Governance hard_stop=True",
        )

    # If needs_review: allow RUN_LLM (to produce explanation / follow-up)
    # unless you want needs_review to mean "stop and human review".
    if needs_review:
        return ExecutionEnvelope(
            allowed_actions={AllowedAction.RUN_LLM, AllowedAction.STOP},
            reason="Governance needs_review=True (allow bounded LLM follow-up)",
        )

    # Normal flow: allow RUN_LLM only if your strategy is "LLM retry allowed",
    # otherwise STOP-only. For Day 32 we keep it permissive but still bounded.
    return ExecutionEnvelope(
        allowed_actions={AllowedAction.RUN_LLM, AllowedAction.STOP},
        reason="Normal flow (LLM follow-up permitted if agent policy triggers it)",
    )