from typing import Dict, List

from stage_status import StageStatus
from stage_result import StageResult
from degradation_mode import DegradationMode


def evaluate_failure_policy(
    det_res: StageResult,
    llm_res: StageResult,
    cc_res: StageResult,
) -> Dict:

    escalation_reasons: List[str] = []

    # Rule 1 — Deterministic failed
    if det_res.status == StageStatus.FAILED:
        escalation_reasons.append("DETERMINISTIC_FAILED")
        return {
            "needs_review": True,
            "degradation_mode": DegradationMode.TOTAL_FAILURE,
            "escalation_reasons": escalation_reasons,
        }

    # Rule 2 — LLM failed but deterministic succeeded
    if (
        det_res.status == StageStatus.SUCCESS
        and llm_res.status == StageStatus.FAILED
    ):
        escalation_reasons.append("LLM_FAILED")
        return {
            "needs_review": True,
            "degradation_mode": DegradationMode.DETERMINISTIC_ONLY,
            "escalation_reasons": escalation_reasons,
        }

    # Rule 3 — Cross-check failed
    if cc_res.status == StageStatus.FAILED:
        escalation_reasons.append("CROSS_CHECK_FAILED")
        return {
            "needs_review": True,
            "degradation_mode": DegradationMode.NO_CROSS_CHECK,
            "escalation_reasons": escalation_reasons,
        }

    # Rule 4 — All good
    return {
        "needs_review": False,
        "degradation_mode": DegradationMode.NONE,
        "escalation_reasons": [],
    }