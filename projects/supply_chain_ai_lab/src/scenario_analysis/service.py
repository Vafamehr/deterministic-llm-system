from simulation_engine.schemas import SimulationResult
from scenario_analysis.schemas import (
    ScenarioAnalysisResult,
    ScenarioComparisonRow,
)


class ScenarioAnalysisService:
    """
    Converts raw simulation results into structured scenario comparisons.
    """

    def analyze(self, simulation_result: SimulationResult) -> ScenarioAnalysisResult:
        if not simulation_result.scenario_results:
            raise ValueError("simulation_result.scenario_results cannot be empty.")

        if simulation_result.baseline_result is None:
            raise ValueError("simulation_result.baseline_result cannot be None.")

        baseline_name = "baseline"
        baseline_replenishment = simulation_result.baseline_result.replenishment_result
        baseline_units = baseline_replenishment.recommended_order_units

        comparison_rows = [
            ScenarioComparisonRow(
                scenario_name=baseline_name,
                reorder=baseline_replenishment.should_reorder,
                recommended_units=baseline_units,
                delta_vs_baseline=0.0,
            )
        ]

        for scenario_result in simulation_result.scenario_results:
            scenario_name = scenario_result.scenario.name

            if scenario_name == baseline_name:
                continue

            replenishment = scenario_result.decision_result.replenishment_result
            scenario_units = replenishment.recommended_order_units
            delta_vs_baseline = scenario_units - baseline_units

            comparison_rows.append(
                ScenarioComparisonRow(
                    scenario_name=scenario_name,
                    reorder=replenishment.should_reorder,
                    recommended_units=scenario_units,
                    delta_vs_baseline=delta_vs_baseline,
                )
            )

        return ScenarioAnalysisResult(
            baseline_scenario_name=baseline_name,
            comparison_rows=comparison_rows,
        )