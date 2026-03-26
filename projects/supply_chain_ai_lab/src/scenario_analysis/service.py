from decision_intelligence.service import classify_decision_intelligence
from simulation_engine.schemas import SimulationResult
from scenario_analysis.schemas import (
    ScenarioAnalysisResult,
    ScenarioComparisonRow,
)


class ScenarioAnalysisService:
    """
    Converts raw simulation results into structured scenario comparisons.
    """

    def _compute_inventory_pressure(self, days_of_supply: float) -> str:
        if days_of_supply < 5:
            return "HIGH"
        if days_of_supply < 10:
            return "MEDIUM"
        return "LOW"

    def _compute_overstock_risk(self, days_of_supply: float) -> str:
        if days_of_supply > 30:
            return "HIGH"
        if days_of_supply >= 20:
            return "MEDIUM"
        return "LOW"

    def analyze(self, simulation_result: SimulationResult) -> ScenarioAnalysisResult:
        if not simulation_result.scenario_results:
            raise ValueError("simulation_result.scenario_results cannot be empty.")

        if simulation_result.baseline_result is None:
            raise ValueError("simulation_result.baseline_result cannot be None.")

        baseline_name = "baseline"

        baseline_replenishment = simulation_result.baseline_result.replenishment_result
        baseline_inventory = simulation_result.baseline_result.inventory_result

        baseline_units = baseline_replenishment.recommended_order_units
        baseline_days_of_supply = baseline_inventory.days_of_supply
        baseline_stockout_risk = baseline_inventory.stockout_risk
        baseline_inventory_pressure = self._compute_inventory_pressure(
            baseline_days_of_supply
        )
        baseline_overstock_risk = self._compute_overstock_risk(
            baseline_days_of_supply
        )
        baseline_decision_intelligence = classify_decision_intelligence(
            days_of_supply=baseline_days_of_supply,
            stockout_risk=baseline_stockout_risk,
            inventory_pressure=baseline_inventory_pressure,
            overstock_risk=baseline_overstock_risk,
        )

        comparison_rows = [
            ScenarioComparisonRow(
                scenario_name=baseline_name,
                reorder=baseline_replenishment.should_reorder,
                recommended_units=baseline_units,
                delta_vs_baseline=0.0,
                days_of_supply=baseline_days_of_supply,
                stockout_risk=baseline_stockout_risk,
                inventory_pressure=baseline_inventory_pressure,
                overstock_risk=baseline_overstock_risk,
                decision_intelligence=baseline_decision_intelligence,
            )
        ]

        for scenario_result in simulation_result.scenario_results:
            scenario_name = scenario_result.scenario.name

            if scenario_name == baseline_name:
                continue

            replenishment = scenario_result.decision_result.replenishment_result
            inventory = scenario_result.decision_result.inventory_result

            scenario_units = replenishment.recommended_order_units
            delta_vs_baseline = scenario_units - baseline_units
            scenario_days_of_supply = inventory.days_of_supply
            scenario_stockout_risk = inventory.stockout_risk
            scenario_inventory_pressure = self._compute_inventory_pressure(
                scenario_days_of_supply
            )
            scenario_overstock_risk = self._compute_overstock_risk(
                scenario_days_of_supply
            )
            scenario_decision_intelligence = classify_decision_intelligence(
                days_of_supply=scenario_days_of_supply,
                stockout_risk=scenario_stockout_risk,
                inventory_pressure=scenario_inventory_pressure,
                overstock_risk=scenario_overstock_risk,
            )

            comparison_rows.append(
                ScenarioComparisonRow(
                    scenario_name=scenario_name,
                    reorder=replenishment.should_reorder,
                    recommended_units=scenario_units,
                    delta_vs_baseline=delta_vs_baseline,
                    days_of_supply=scenario_days_of_supply,
                    stockout_risk=scenario_stockout_risk,
                    inventory_pressure=scenario_inventory_pressure,
                    overstock_risk=scenario_overstock_risk,
                    decision_intelligence=scenario_decision_intelligence,
                )
            )

        return ScenarioAnalysisResult(
            baseline_scenario_name=baseline_name,
            comparison_rows=comparison_rows,
        )