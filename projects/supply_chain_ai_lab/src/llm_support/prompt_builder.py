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
        f"- overstock_risk: {context.baseline_overstock_risk}\n"
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
                f"inventory_pressure={row.inventory_pressure}, "
                f"overstock_risk={row.overstock_risk}"
            )
        )

    scenario_block = "SCENARIO RESULTS\n" + "\n".join(scenario_lines)

    system_note_block = ""
    if context.system_note is not None and context.system_note.strip():
        system_note_block = f"SYSTEM NOTE\n- {context.system_note}\n"

    if request.task == ExplanationTask.SIMULATION_SUMMARY:
        task_instruction = (
            "TASK\n"
            "Write a short simulation summary using only the structured results.\n"
        )
    elif request.task == ExplanationTask.SCENARIO_COMPARISON:
        task_instruction = (
            "TASK\n"
            "Compare the scenarios against baseline using only the structured results.\n"
        )
    elif request.task == ExplanationTask.RISK_EXPLANATION:
        task_instruction = (
            "TASK\n"
            "Explain the main operational risks using only the structured results.\n"
        )
    else:
        raise ValueError(f"Unsupported explanation task: {request.task}")

    output_contract_block = (
        "OUTPUT FORMAT\n"
        "Return plain text only.\n"
        "Return EXACTLY these 3 labels and nothing else:\n"
        "SUMMARY\n"
        "SCENARIO CHANGES\n"
        "RISK TAKEAWAY\n"
        "\n"
        "FORMAT RULES\n"
        "- Do not use markdown.\n"
        "- Do not use **, *, -, or numbered lists in the final answer.\n"
        "- Write the label on its own line.\n"
        "- Put the content for that label on the next line.\n"
        "- SUMMARY: exactly 1 sentence.\n"
        "- SCENARIO CHANGES: exactly 2 sentences.\n"
        "- RISK TAKEAWAY: exactly 1 sentence.\n"
        "- If multiple non-baseline scenarios are present, mention all of them in SCENARIO CHANGES.\n"
        "- Total output must stay under 110 words.\n"
    )

    guardrail_block = (
        "GUARDRAILS\n"
        "- Do not invent facts.\n"
        "- Do not mention data that is not provided.\n"
        "- Do not make decisions for the system.\n"
        "- Do not add introductions or conclusions.\n"
        "- Do not use any heading other than SUMMARY, SCENARIO CHANGES, and RISK TAKEAWAY.\n"
        "- The deterministic outputs are the source of truth.\n"
        "- Keep the explanation concise and operationally grounded.\n"
    )

    prompt = (
        f"{task_instruction}\n"
        f"{output_contract_block}\n"
        f"{baseline_block}\n"
        f"{scenario_block}\n"
        f"{system_note_block}\n"
        f"{guardrail_block}"
    )

    return prompt