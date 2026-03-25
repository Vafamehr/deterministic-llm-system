from __future__ import annotations

from llm_support.schemas import ExplanationRequest, ExplanationTask


def build_explanation_prompt(request: ExplanationRequest) -> str:
    context = request.context

    baseline_block = (
        "BASELINE STATE\n"
        f"- reorder: {context.baseline_reorder}\n"
        f"- recommended_units: {context.baseline_recommended_units:.2f}\n"
        f"- days_of_supply: {context.baseline_days_of_supply:.2f}\n"
        f"- stockout_risk: {context.baseline_stockout_risk}\n"
        f"- inventory_pressure: {context.baseline_inventory_pressure}\n"
    )

    scenario_lines = []
    for row in context.scenario_rows:
        scenario_lines.append(
            (
                f"- {row.scenario_name}: "
                f"reorder={row.reorder}, "
                f"recommended_units={row.recommended_units:.2f}, "
                f"delta_vs_baseline={row.delta_vs_baseline:.2f}, "
                f"days_of_supply={row.days_of_supply:.2f}, "
                f"stockout_risk={row.stockout_risk}, "
                f"inventory_pressure={row.inventory_pressure}"
            )
        )

    scenario_block = "SCENARIO RESULTS\n" + "\n".join(scenario_lines)

    system_note_block = ""
    if context.system_note is not None and context.system_note.strip():
        system_note_block = f"\nSYSTEM NOTE\n- {context.system_note}\n"

    task_instruction = ""
    if request.task == ExplanationTask.SIMULATION_SUMMARY:
        task_instruction = (
            "TASK\n"
            "Write a short grounded summary of the simulation results. "
            "Explain what changed from baseline across scenarios using only the provided structured outputs.\n"
        )
    elif request.task == ExplanationTask.SCENARIO_COMPARISON:
        task_instruction = (
            "TASK\n"
            "Compare the scenarios against the baseline. "
            "Highlight the main differences in reorder behavior, recommended units, inventory pressure, "
            "days of supply, and stockout risk using only the provided structured outputs.\n"
        )
    elif request.task == ExplanationTask.RISK_EXPLANATION:
        task_instruction = (
            "TASK\n"
            "Explain the main operational risks shown by the simulation outputs. "
            "Focus on stockout risk, inventory pressure, days of supply, and why recommended units changed.\n"
        )
    else:
        raise ValueError(f"Unsupported explanation task: {request.task}")

    guardrail_block = (
        "GUARDRAILS\n"
        "- Do not invent facts.\n"
        "- Do not mention data that is not provided.\n"
        "- Do not make decisions for the system.\n"
        "- The deterministic outputs are the source of truth.\n"
        "- Keep the explanation concise and operationally grounded.\n"
    )

    prompt = (
        f"{task_instruction}\n"
        f"{baseline_block}\n"
        f"{scenario_block}\n"
        f"{system_note_block}\n"
        f"{guardrail_block}"
    )

    return prompt