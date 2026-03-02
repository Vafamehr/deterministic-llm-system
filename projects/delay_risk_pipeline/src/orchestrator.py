from __future__ import annotations

import time
from typing import Dict, List, Optional

from router.dispatch import choose_branch
from router.strategy import Strategy

from decision_engine import assess_risk_from_packets
from llm_reasoner import build_prompt, call_llm_with_retry
from execution_plan import ExecutionPlan

from stage_result import StageResult
from stage_status import StageStatus

from failure_policy import evaluate_failure_policy

from agent_controller import AgentController
from agent_action import AgentAction

from decision_trace import DecisionTrace
from governance_to_envelope import build_execution_envelope

from types import MappingProxyType


def run_pipeline(fact_packets: List[str]) -> Dict:
    """
    Public entrypoint for the system.
    Keep this name stable; internals can evolve.
    """
    return run_full_assessment(fact_packets)


# ------------------------------------------------------------
# Internal stage runners
# ------------------------------------------------------------

def _run_deterministic(fact_packets: List[str]) -> StageResult:
    t0 = time.perf_counter()
    try:
        result = assess_risk_from_packets(fact_packets)
        latency_ms = (time.perf_counter() - t0) * 1000
        return StageResult(
            status=StageStatus.SUCCESS,
            data=result,
            error=None,
            latency_ms=latency_ms,
        )
    except Exception as e:
        latency_ms = (time.perf_counter() - t0) * 1000
        return StageResult(
            status=StageStatus.FAILED,
            data=None,
            error=str(e),
            latency_ms=latency_ms,
        )


def _run_llm(fact_packets: List[str]) -> StageResult:
    t0 = time.perf_counter()
    try:
        prompt = build_prompt(fact_packets)
        result = call_llm_with_retry(prompt)
        latency_ms = (time.perf_counter() - t0) * 1000
        return StageResult(
            status=StageStatus.SUCCESS,
            data=result,
            error=None,
            latency_ms=latency_ms,
        )
    except Exception as e:
        latency_ms = (time.perf_counter() - t0) * 1000
        return StageResult(
            status=StageStatus.FAILED,
            data=None,
            error=str(e),
            latency_ms=latency_ms,
        )


def _cross_check(det_result: StageResult, llm_result: StageResult) -> StageResult:
    """
    Compare deterministic vs LLM project risks.
    """
    if det_result.status != StageStatus.SUCCESS or llm_result.status != StageStatus.SUCCESS:
        return StageResult(
            status=StageStatus.SKIPPED,
            data=None,
            error="Skipped cross-check because upstream stage failed or was skipped.",
            latency_ms=0.0,
        )

    t0 = time.perf_counter()
    try:
        deterministic_result: Dict = det_result.data or {}
        llm_result_data: Dict = llm_result.data or {}

        deterministic_projects = {
            item["fact_packet"]: item["risk_level"]
            for item in deterministic_result.get("assessments", [])
        }

        inconsistencies: List[Dict] = []
        for proj in llm_result_data.get("projects", []):
            project_id = proj.get("project_id")
            if not project_id:
                continue

            for packet, det_risk in deterministic_projects.items():
                if f"Project: {project_id}" in packet:
                    if proj.get("risk") != det_risk:
                        inconsistencies.append(
                            {
                                "project_id": project_id,
                                "deterministic_risk": det_risk,
                                "llm_risk": proj.get("risk"),
                            }
                        )

        total = len(llm_result_data.get("projects", []))
        consistency_ratio = 1.0 if total == 0 else 1 - (len(inconsistencies) / total)

        confidence = "HIGH"
        if consistency_ratio < 1.0:
            confidence = "MEDIUM"
        if consistency_ratio < 0.5:
            confidence = "LOW"

        payload = {
            "inconsistencies": inconsistencies,
            "consistency_ratio": consistency_ratio,
            "confidence": confidence,
        }

        latency_ms = (time.perf_counter() - t0) * 1000
        return StageResult(
            status=StageStatus.SUCCESS,
            data=payload,
            error=None,
            latency_ms=latency_ms,
        )

    except Exception as e:
        latency_ms = (time.perf_counter() - t0) * 1000
        return StageResult(
            status=StageStatus.FAILED,
            data=None,
            error=str(e),
            latency_ms=latency_ms,
        )


def _build_execution_plan(strategy: Strategy) -> ExecutionPlan:
    if strategy == Strategy.ANALYTICS:
        return ExecutionPlan(run_deterministic=True, run_llm=False, run_cross_check=False)
    if strategy == Strategy.SUMMARY:
        return ExecutionPlan(run_deterministic=False, run_llm=True, run_cross_check=False)
    if strategy == Strategy.POLICY:
        return ExecutionPlan(run_deterministic=True, run_llm=True, run_cross_check=True)
    return ExecutionPlan(run_deterministic=True, run_llm=True, run_cross_check=True)


def _stage_result_to_dict(r: StageResult) -> Dict:
    return {
        "status": r.status.value,
        "error": r.error,
        "latency_ms": r.latency_ms,
    }


def _apply_governance_to_confidence(governance: dict, confidence: Optional[str]) -> str:
    if governance.get("needs_review") is True:
        if confidence == "HIGH" or confidence is None:
            return "MEDIUM"
    return confidence or "MEDIUM"


def _summarize_trace_for_agent(trace: DecisionTrace) -> Dict:
    events = trace.to_dict()
    return {
        "steps_run": [e["step"] for e in events],
        "had_early_exit": any(e["step"] == "early_exit" for e in events),
        "llm_attempted": any(e["step"] in ("llm", "followup_llm") for e in events),
        "governance_checks": sum(1 for e in events if "governance" in e["step"]),
        "last_step": events[-1]["step"] if events else None,
    }


def _build_output(
    *,
    strategy,
    plan,
    det_res,
    llm_res,
    cc_res,
    governance,
    inconsistencies,
    confidence,
    consistency_ratio,
    deterministic_ms,
    llm_ms,
    total_ms,
    trace,
    step_budget=None,  # Day 33: orchestrator-owned budget in output contract
    agent=None,
    decision=None,
    force_run_llm=None,
    force_run_cross_check=None,
) -> Dict:
    """
    Single output contract for BOTH normal path and early-exit path.
    Keeps the API stable as run_full_assessment evolves.
    """
    run_llm = plan.run_llm if force_run_llm is None else force_run_llm
    run_cc = plan.run_cross_check if force_run_cross_check is None else force_run_cross_check

    out = {
        "strategy": strategy.value,
        "execution_plan": {
            "run_deterministic": plan.run_deterministic,
            "run_llm": run_llm,
            "run_cross_check": run_cc,
        },
        "stage_results": {
            "deterministic": _stage_result_to_dict(det_res),
            "llm": _stage_result_to_dict(llm_res),
            "cross_check": _stage_result_to_dict(cc_res),
        },
        "governance": governance,
        "deterministic_layer": det_res.data if det_res.status == StageStatus.SUCCESS else None,
        "llm_layer": llm_res.data if llm_res.status == StageStatus.SUCCESS else None,
        "inconsistencies": inconsistencies,
        "confidence": confidence,
        "consistency_ratio": consistency_ratio,
        "metrics": {
            "deterministic_ms": deterministic_ms,
            "llm_ms": llm_ms,
            "total_ms": total_ms,
        },
        "decision_trace": trace.to_dict(),
    }

    if agent is not None and decision is not None:
        out["agent"] = {
            "step_budget": step_budget,
            "decision": {
                "action": decision.action.value,
                "reason": decision.reason,
                "requested_by": getattr(decision, "requested_by", None),
                "step_index": getattr(decision, "step_index", None),
            },
        }

    return out


# ------------------------------------------------------------
# Day 33: Metered decision window helper (single source of truth)
# ------------------------------------------------------------

def _run_metered_decision_window(
    *,
    agent: AgentController,
    step_budget: int,
    trace: DecisionTrace,
    trace_context: Dict,
    envelope,
    det_res: StageResult,
    llm_res: StageResult,
    cc_res: StageResult,
    governance: Dict,
) -> Dict:
    """
    Day 33: orchestrator schedules Step 0 and optional Step 1.
    No loops. No recursion. Same inputs, only step_index changes.
    Returns dict with decision + decision_1 for provenance.
    """
    goal = "Produce a safe, governance-aligned assessment"

    stage_results = {
        "deterministic": _stage_result_to_dict(det_res),
        "llm": _stage_result_to_dict(llm_res),
        "cross_check": _stage_result_to_dict(cc_res),
    }

    governance_context = {
        "needs_review": governance.get("needs_review", False),
        "hard_stop": governance.get("hard_stop", False),
        "degradation_mode": governance.get("degradation_mode"),
    }

    decision_0 = agent.decide(
        goal=goal,
        step_index=0,
        step_budget=step_budget,
        stage_results=stage_results,
        trace_context=trace_context,
        governance_context=governance_context,
        envelope=envelope,
    )

    # Day 34 (Chunk 1): bounded, read-only delta derived from decision_0

    delta_context = MappingProxyType({
        "proposed_action": decision_0.action.value,
        "reasoning_summary": decision_0.reason,
        "llm_already_ran": bool(stage_results.get("llm")),
        "known_constraints": {
            "allowed_actions": sorted(a.value for a in envelope.allowed_actions),
            "hard_stop": bool(governance_context.get("hard_stop", False)),
            "needs_review": bool(governance_context.get("needs_review", False)),
            "degradation_mode": governance_context.get("degradation_mode"),
        },
    })


    decision_1 = None
    if decision_0.action == AgentAction.RUN_LLM and step_budget > 1:
        trace.add_event(
            step="decision_1_confirmation_input",
            status="ok",
            reason="delta_context_provided",
            data_snapshot={
                "mode": "confirm_delta",
                "proposed_action": delta_context.get("proposed_action"),
                "llm_already_ran": delta_context.get("llm_already_ran"),
                "known_constraints": delta_context.get("known_constraints"),
                "reasoning_summary_preview": str(delta_context.get("reasoning_summary", ""))[:200],
            },
        )
        decision_1 = agent.decide(
            goal=goal,
            step_index=1,
            step_budget=step_budget,
            stage_results=stage_results,
            trace_context=trace_context,
            governance_context=governance_context,
            envelope=envelope,
            delta_context=delta_context,
        )
        trace.add_event(
        step="decision_1_confirmation_result",
        status="ok",
        reason="confirmation_pass_complete",
        data_snapshot={
            "step_0_action": decision_0.action.value,
            "step_1_action": decision_1.action.value,
            "step_1_agrees_with_step_0": decision_1.action == decision_0.action,
        },
    )

    decision = decision_1 or decision_0

    trace.add_event(
        step="metered_reasoning_window",
        status="ok",
        reason="orchestrator_scheduled_steps",
        data_snapshot={
            "step_budget": step_budget,
            "ran_step_0": True,
            "ran_step_1": decision_1 is not None,
            "final_decision": decision.action.value,
            "final_from_step": 1 if decision_1 is not None else 0,
        },
    )

    trace.add_event(
        step="agent_decision",
        status=decision.action.value,
        reason=decision.reason,
        data_snapshot={
            "requested_by": getattr(decision, "requested_by", None),
            "step_index": getattr(decision, "step_index", None),
            "step_budget": step_budget,
        },
    )

    # Day 36: Commit Boundary Marker
    trace.add_event(
    step="decision_commit_boundary",
    status="committed",
    reason="metered_window_closed",
    data_snapshot={
        "final_action": decision.action.value,
        "from_step": 1 if decision_1 is not None else 0,
        "step_budget": step_budget,
    },
)

    return {"decision": decision, "decision_1": decision_1}


# ------------------------------------------------------------
# Main orchestrator
# ------------------------------------------------------------

def _run_stages(
    *,
    fact_packets: List[str],
    plan,
    det_res: StageResult,
    llm_res: StageResult,
    cc_res: StageResult,
    trace: DecisionTrace,
    start_total: float,
):
    """
    Runs deterministic/LLM/cross-check stages based on the ExecutionPlan.
    Handles early-exit and traces stage outcomes.
    """
    inconsistencies = []
    consistency_ratio = None
    confidence = None

    deterministic_ms = None
    llm_ms = None
    llm_ran = False
    early_exit_taken = False

    # --- Deterministic ---
    if plan.run_deterministic:
        start = time.perf_counter()
        det_res = _run_deterministic(fact_packets)
        deterministic_ms = (time.perf_counter() - start) * 1000

        trace.add_event(
            step="deterministic",
            status=det_res.status.value,
            reason="Deterministic stage completed" if det_res.status == StageStatus.SUCCESS else "Deterministic stage not successful",
            data_snapshot={"latency_ms": deterministic_ms},
        )

    # --- Early Exit Optimization (only if deterministic succeeded) ---
    if plan.run_llm and det_res.status == StageStatus.SUCCESS:
        assessments = (det_res.data or {}).get("assessments", [])
        if assessments and all(item.get("risk_level") == "LOW" for item in assessments):
            early_exit_taken = True

            llm_res = StageResult(
                status=StageStatus.SKIPPED,
                data=None,
                error="Skipped LLM due to early-exit: all deterministic risks LOW.",
                latency_ms=0.0,
            )
            cc_res = StageResult(
                status=StageStatus.SKIPPED,
                data=None,
                error="Skipped cross-check because LLM was skipped by early-exit.",
                latency_ms=0.0,
            )
            confidence = "HIGH"
            consistency_ratio = 1.0

            total_ms = (time.perf_counter() - start_total) * 1000

            trace.add_event(
                step="early_exit",
                status="taken",
                reason="All deterministic risks LOW; skipped LLM and cross-check",
                data_snapshot={},
            )

            return (
                det_res, llm_res, cc_res,
                inconsistencies, consistency_ratio, confidence,
                deterministic_ms, llm_ms, total_ms,
                llm_ran, early_exit_taken,
            )

    # --- LLM ---
    if plan.run_llm:
        start = time.perf_counter()
        llm_res = _run_llm(fact_packets)
        llm_ms = (time.perf_counter() - start) * 1000
        llm_ran = True

        trace.add_event(
            step="llm",
            status=llm_res.status.value,
            reason="LLM stage completed" if llm_res.status == StageStatus.SUCCESS else "LLM stage not successful",
            data_snapshot={"latency_ms": llm_ms},
        )

    # --- Cross-check ---
    if plan.run_cross_check:
        cc_res = _cross_check(det_res, llm_res)

        if cc_res.status == StageStatus.SUCCESS:
            cc = cc_res.data or {}
            inconsistencies = cc.get("inconsistencies", [])
            consistency_ratio = cc.get("consistency_ratio")
            confidence = cc.get("confidence")

        trace.add_event(
            step="cross_check",
            status=cc_res.status.value,
            reason="Cross-check completed" if cc_res.status == StageStatus.SUCCESS else "Cross-check not successful",
            data_snapshot={
                "inconsistencies_count": len(inconsistencies or []),
                "consistency_ratio": consistency_ratio,
            },
        )

    # --- Confidence defaults ---
    if confidence is None:
        if plan.run_deterministic and not plan.run_llm:
            confidence = "HIGH"
            consistency_ratio = 1.0
        elif plan.run_llm and not plan.run_cross_check:
            confidence = "MEDIUM"

    total_ms = (time.perf_counter() - start_total) * 1000

    return (
        det_res, llm_res, cc_res,
        inconsistencies, consistency_ratio, confidence,
        deterministic_ms, llm_ms, total_ms,
        llm_ran, early_exit_taken,
    )


def run_full_assessment(fact_packets: List[str]) -> Dict:
    # ============================================================
    # ## 1) Routing + plan (deterministic entry)
    # ============================================================
    routing_input = " ".join(fact_packets[:3])
    trace = DecisionTrace()

    try:
        strategy = choose_branch(routing_input)
    except Exception:
        strategy = Strategy.GENERAL

    plan = _build_execution_plan(strategy)

    # ============================================================
    # ## 2) Init state (stage defaults + timers)
    # ============================================================
    det_res: StageResult = StageResult(status=StageStatus.SKIPPED, data=None, error=None, latency_ms=0.0)
    llm_res: StageResult = StageResult(status=StageStatus.SKIPPED, data=None, error=None, latency_ms=0.0)
    cc_res: StageResult = StageResult(status=StageStatus.SKIPPED, data=None, error=None, latency_ms=0.0)

    inconsistencies = []
    consistency_ratio = None
    confidence = None
    deterministic_ms = None
    llm_ms = None

    start_total = time.perf_counter()

    (
        det_res, llm_res, cc_res,
        inconsistencies, consistency_ratio, confidence,
        deterministic_ms, llm_ms, total_ms,
        llm_ran, early_exit_taken,
    ) = _run_stages(
        fact_packets=fact_packets,
        plan=plan,
        det_res=det_res,
        llm_res=llm_res,
        cc_res=cc_res,
        trace=trace,
        start_total=start_total,
    )

    # ============================================================
    # ## 3) Governance (always) + metered decision window
    # ============================================================
    step_budget = 2  # Day 33: controlled multi-step capacity (leased by orchestrator)

    governance = evaluate_failure_policy(det_res, llm_res, cc_res)
    if hasattr(governance.get("degradation_mode"), "value"):
        governance["degradation_mode"] = governance["degradation_mode"].value

    trace.add_event(
        step="governance",
        status="review" if governance.get("needs_review") else "pass",
        reason="Failure policy evaluated" + (" (early-exit)" if early_exit_taken else ""),
        data_snapshot={
            "degradation_mode": governance.get("degradation_mode"),
            "hard_stop": governance.get("hard_stop", False),
            "escalation_reasons": governance.get("escalation_reasons", []),
        },
    )

    confidence = _apply_governance_to_confidence(governance, confidence)

    agent = AgentController()

    trace_context = _summarize_trace_for_agent(trace)
    trace_context["llm_attempted"] = bool(llm_ran)  # force truth from pipeline state

    envelope = build_execution_envelope(governance)

    window = _run_metered_decision_window(
        agent=agent,
        step_budget=step_budget,
        trace=trace,
        trace_context=trace_context,
        envelope=envelope,
        det_res=det_res,
        llm_res=llm_res,
        cc_res=cc_res,
        governance=governance,
    )
    decision = window["decision"]

    # ============================================================
    # ## 4) Follow-up execution (still bounded by governance)
    # ============================================================
    hard_stop = governance.get("hard_stop", False)

    if (not early_exit_taken) and (not hard_stop) and (decision.action == AgentAction.RUN_LLM) and (not llm_ran):
        start = time.perf_counter()
        llm_res = _run_llm(fact_packets)
        llm_ms = (time.perf_counter() - start) * 1000
        llm_ran = True

        trace.add_event(
            step="followup_llm",
            status=llm_res.status.value,
            reason="Agent-triggered follow-up LLM run",
            data_snapshot={"latency_ms": llm_ms},
        )

        if plan.run_cross_check:
            cc_res = _cross_check(det_res, llm_res)

            if cc_res.status == StageStatus.SUCCESS:
                cc = cc_res.data or {}
                inconsistencies = cc.get("inconsistencies", [])
                consistency_ratio = cc.get("consistency_ratio")
                confidence = cc.get("confidence")

            trace.add_event(
                step="followup_cross_check",
                status=cc_res.status.value,
                reason="Cross-check re-run after follow-up LLM",
                data_snapshot={
                    "inconsistencies_count": len(inconsistencies or []),
                    "consistency_ratio": consistency_ratio,
                },
            )

        governance = evaluate_failure_policy(det_res, llm_res, cc_res)
        if hasattr(governance.get("degradation_mode"), "value"):
            governance["degradation_mode"] = governance["degradation_mode"].value

        trace.add_event(
            step="governance_recheck",
            status="review" if governance.get("needs_review") else "pass",
            reason="Governance re-evaluated after follow-up",
            data_snapshot={
                "degradation_mode": governance.get("degradation_mode"),
                "hard_stop": governance.get("hard_stop", False),
                "escalation_reasons": governance.get("escalation_reasons", []),
            },
        )

        confidence = _apply_governance_to_confidence(governance, confidence)

    # ============================================================
    # ## 5) Final output (single contract)
    # ============================================================
    return _build_output(
        strategy=strategy,
        plan=plan,
        det_res=det_res,
        llm_res=llm_res,
        cc_res=cc_res,
        governance=governance,
        inconsistencies=inconsistencies,
        confidence=confidence,
        consistency_ratio=consistency_ratio,
        deterministic_ms=deterministic_ms,
        llm_ms=llm_ms,
        total_ms=total_ms,
        trace=trace,
        step_budget=step_budget,
        agent=agent,
        decision=decision,
    )