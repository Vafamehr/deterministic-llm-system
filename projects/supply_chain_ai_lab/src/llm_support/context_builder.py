from __future__ import annotations

from llm_support.schemas import ExplanationContext, ScenarioExplanationRow
from scenario_analysis.schemas import ScenarioAnalysisResult


def build_explanation_context(
    analysis_result: ScenarioAnalysisResult,
) -> ExplanationContext:
    # --- Find baseline row ---
    baseline_row = next(
        row
        for row in analysis_result.comparison_rows
        if row.scenario_name == "baseline"
    )

    # --- Build scenario rows ---
    scenario_rows = [
        ScenarioExplanationRow(
            scenario_name=row.scenario_name,
            reorder=row.reorder,
            recommended_units=row.recommended_units,
            delta_vs_baseline=row.delta_vs_baseline,
            days_of_supply=row.days_of_supply,
            stockout_risk=row.stockout_risk,
            inventory_pressure=row.inventory_pressure,
            overstock_risk=row.overstock_risk,
        )
        for row in analysis_result.comparison_rows
    ]

    # --- Build explanation context ---
    return ExplanationContext(
        baseline_reorder=baseline_row.reorder,
        baseline_recommended_units=baseline_row.recommended_units,
        baseline_days_of_supply=baseline_row.days_of_supply,
        baseline_stockout_risk=baseline_row.stockout_risk,
        baseline_inventory_pressure=baseline_row.inventory_pressure,
        baseline_overstock_risk=baseline_row.overstock_risk,
        scenario_rows=scenario_rows,
        system_note="Deterministic outputs are the source of truth. LLM output is explanation only.",
    )