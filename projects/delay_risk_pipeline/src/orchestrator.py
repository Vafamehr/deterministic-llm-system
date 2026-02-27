from __future__ import annotations

from typing import Dict, List

from router.dispatch import choose_branch
from router.strategy import Strategy

from decision_engine import assess_risk_from_packets
from llm_reasoner import build_prompt, call_llm_with_retry
from execution_plan import ExecutionPlan
import time
from stage_result import StageResult
from stage_status import StageStatus

from failure_policy import evaluate_failure_policy


from agent_controller import AgentController
from agent_action import AgentAction

from decision_trace import DecisionTrace

from governance_to_envelope import build_execution_envelope

# trace = DecisionTrace()




def run_pipeline(fact_packets: List[str]) -> Dict:
    """
    Public entrypoint for the system.
    Keep this name stable; internals can evolve.
    """
    return run_full_assessment(fact_packets)


# ------------------------------------------------------------
# Internal helpers (keep orchestrator composable)
# ------------------------------------------------------------



# modified to the following version: 
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






##### 
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



### Wrap _cross_check with Failure Boundary + Upstream Gating


def _cross_check(det_result: StageResult, llm_result: StageResult) -> StageResult:
    """
    Compare deterministic vs LLM project risks.

    StageResult.data on SUCCESS:
      {
        "inconsistencies": List[Dict],
        "consistency_ratio": float,
        "confidence": str
      }
    """
    # Gate: only cross-check when upstream stages are SUCCESS
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
        return ExecutionPlan(
            run_deterministic=True,
            run_llm=False,
            run_cross_check=False,
        )

    if strategy == Strategy.SUMMARY:
        return ExecutionPlan(
            run_deterministic=False,
            run_llm=True,
            run_cross_check=False,
        )

    if strategy == Strategy.POLICY:
        return ExecutionPlan(
            run_deterministic=True,
            run_llm=True,
            run_cross_check=True,
        )

    # GENERAL fallback
    return ExecutionPlan(
        run_deterministic=True,
        run_llm=True,
        run_cross_check=True,
    )







def _stage_result_to_dict(r: StageResult) -> Dict:
    return {
        "status": r.status.value,
        "error": r.error,
        "latency_ms": r.latency_ms,
    }




def _apply_governance_to_confidence(governance: dict, confidence: str | None) -> str:
    # If system says "needs review", confidence cannot be HIGH.
    if governance.get("needs_review") is True:
        if confidence == "HIGH" or confidence is None:
            return "MEDIUM"
    return confidence or "MEDIUM"


def _summarize_trace_for_agent(trace: DecisionTrace) -> Dict:
    """
    Provide a minimal, structured summary of what has already happened.
    We intentionally avoid passing the full trace to keep decisions bounded.
    """

    events = trace.to_dict()

    summary = {
        "steps_run": [e["step"] for e in events],
        "had_early_exit": any(e["step"] == "early_exit" for e in events),
        "llm_attempted": any(e["step"] in ("llm", "followup_llm") for e in events),
        "governance_checks": sum(1 for e in events if "governance" in e["step"]),
        "last_step": events[-1]["step"] if events else None,
    }

    return summary

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
            "max_steps": agent.max_steps,
            "decision": {
                "action": decision.action.value,
                "reason": decision.reason,
                "requested_by": decision.requested_by,
                "step_index": decision.step_index,
            },
        }

    return out


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
    Returns:
      det_res, llm_res, cc_res,
      inconsistencies, consistency_ratio, confidence,
      deterministic_ms, llm_ms, total_ms,
      llm_ran, early_exit_taken
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
            status=det_res.status.value if hasattr(det_res.status, "value") else str(det_res.status),
            reason="Deterministic stage completed"
            if det_res.status == StageStatus.SUCCESS
            else "Deterministic stage not successful",
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
            status=llm_res.status.value if hasattr(llm_res.status, "value") else str(llm_res.status),
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
            status=cc_res.status.value if hasattr(cc_res.status, "value") else str(cc_res.status),
            reason="Cross-check completed" if cc_res.status == StageStatus.SUCCESS else "Cross-check not successful",
            data_snapshot={
                "inconsistencies_count": len(inconsistencies or []),
                "consistency_ratio": consistency_ratio,
            },
        )

    # --- Confidence defaults (same intent as your original) ---
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
    # === 1) ROUTING + PLAN ===
    routing_input = " ".join(fact_packets[:3])
    trace = DecisionTrace()

    try:
        strategy = choose_branch(routing_input)
    except Exception:
        strategy = Strategy.GENERAL

    plan = _build_execution_plan(strategy)

    # === 2) INIT STATE (stage defaults + outputs + metrics + timers) ===
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

    # === 3) EARLY EXIT PATH (still run governance + agent decision, but do not run follow-up stages) ===
    if early_exit_taken:
        governance = evaluate_failure_policy(det_res, llm_res, cc_res)
        
        if hasattr(governance.get("degradation_mode"), "value"):
            governance["degradation_mode"] = governance["degradation_mode"].value

        trace.add_event(
            step="governance",
            status="review" if governance.get("needs_review") else "pass",
            reason="Failure policy evaluated (early-exit)",
            data_snapshot={
                "degradation_mode": governance.get("degradation_mode"),
                "hard_stop": governance.get("hard_stop", False),
                "escalation_reasons": governance.get("escalation_reasons", []),
            },
        )

        confidence = _apply_governance_to_confidence(governance, confidence)

        agent = AgentController(max_steps=1)

        trace_context = _summarize_trace_for_agent(trace)
        # Force truth from the pipeline state (prevents trace mismatches)
        trace_context["llm_attempted"] = bool(llm_ran)

        envelope = build_execution_envelope(governance)

        decision = agent.decide(
            goal="Produce a safe, governance-aligned assessment",
            step_index=0,
            stage_results={
                "deterministic": _stage_result_to_dict(det_res),
                "llm": _stage_result_to_dict(llm_res),
                "cross_check": _stage_result_to_dict(cc_res),
            },
            trace_context=trace_context,
            governance_context={
                "needs_review": governance.get("needs_review", False),
                "hard_stop": governance.get("hard_stop", False),
                "degradation_mode": governance.get("degradation_mode"),
            },
            envelope=envelope,
        )

        trace.add_event(
            step="agent_decision",
            status=decision.action.value,
            reason=decision.reason,
            data_snapshot={
                "requested_by": decision.requested_by,
                "step_index": decision.step_index,
                "max_steps": agent.max_steps,
            },
        )

        return _build_output(
            strategy=strategy,
            plan=plan,
            det_res=det_res,
            llm_res=llm_res,
            cc_res=cc_res,
            governance=governance,
            inconsistencies=[],
            confidence=confidence,
            consistency_ratio=consistency_ratio,
            deterministic_ms=deterministic_ms,
            llm_ms=llm_ms,  # was None in your snippet; keep real value if present
            total_ms=total_ms,
            trace=trace,
            agent=agent,
            decision=decision,
            force_run_llm=False,
            force_run_cross_check=False,
        )

    # === 4) GOVERNANCE + AGENT CONTROL (policy / decision / follow-up / recheck) ===
    total_ms = (time.perf_counter() - start_total) * 1000
    governance = evaluate_failure_policy(det_res, llm_res, cc_res)
    # governance["hard_stop"] = True  #TODO: delete after test TEMP TEST LINE
    if hasattr(governance.get("degradation_mode"), "value"):
        governance["degradation_mode"] = governance["degradation_mode"].value

    trace.add_event(
        step="governance",
        status="review" if governance.get("needs_review") else "pass",
        reason="Failure policy evaluated",
        data_snapshot={
            "degradation_mode": governance.get("degradation_mode"),
            "hard_stop": governance.get("hard_stop", False),
            "escalation_reasons": governance.get("escalation_reasons", []),
        },
    )

    confidence = _apply_governance_to_confidence(governance, confidence)

    agent = AgentController(max_steps=1)

    trace_context = _summarize_trace_for_agent(trace)
    # Force truth from the pipeline state (prevents trace mismatches)
    trace_context["llm_attempted"] = bool(llm_ran)

    envelope = build_execution_envelope(governance)

    decision = agent.decide(
        goal="Produce a safe, governance-aligned assessment",
        step_index=0,
        stage_results={
            "deterministic": _stage_result_to_dict(det_res),
            "llm": _stage_result_to_dict(llm_res),
            "cross_check": _stage_result_to_dict(cc_res),
        },
        trace_context=trace_context,
        governance_context={
            "needs_review": governance.get("needs_review", False),
            "hard_stop": governance.get("hard_stop", False),
            "degradation_mode": governance.get("degradation_mode"),
        },
        envelope=envelope,
    )

    trace.add_event(
        step="agent_decision",
        status=decision.action.value,
        reason=decision.reason,
        data_snapshot={
            "requested_by": decision.requested_by,
            "step_index": decision.step_index,
            "max_steps": agent.max_steps,
        },
    )

    hard_stop = governance.get("hard_stop", False)

    # Follow-up: agent can request one extra LLM execution
    if (not hard_stop) and (decision.action == AgentAction.RUN_LLM) and (not llm_ran):
        start = time.perf_counter()
        llm_res = _run_llm(fact_packets)
        llm_ms = (time.perf_counter() - start) * 1000
        llm_ran = True

        trace.add_event(
            step="followup_llm",
            status=llm_res.status.value if hasattr(llm_res.status, "value") else str(llm_res.status),
            reason="Agent-triggered follow-up LLM run",
            data_snapshot={"latency_ms": llm_ms},
        )

        # If cross-check is part of the plan, re-run it now that LLM exists
        if plan.run_cross_check:
            cc_res = _cross_check(det_res, llm_res)

            if cc_res.status == StageStatus.SUCCESS:
                cc = cc_res.data or {}
                inconsistencies = cc.get("inconsistencies", [])
                consistency_ratio = cc.get("consistency_ratio")
                confidence = cc.get("confidence")

            trace.add_event(
                step="followup_cross_check",
                status=cc_res.status.value if hasattr(cc_res.status, "value") else str(cc_res.status),
                reason="Cross-check re-run after follow-up LLM",
                data_snapshot={
                    "inconsistencies_count": len(inconsistencies or []),
                    "consistency_ratio": consistency_ratio,
                },
            )

        # Re-evaluate governance + confidence after follow-up
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

    # === 5) FINAL OUTPUT (single contract) ===
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
        agent=agent,
        decision=decision,
    )

