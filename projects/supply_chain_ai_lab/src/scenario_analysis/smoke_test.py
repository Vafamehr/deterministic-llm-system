"""
Smoke test for the Scenario Analysis module.

This test runs the simulation engine on a small mock supply chain world,
then converts the raw simulation output into structured scenario comparisons.
"""

from datetime import date

from demand_forecasting.schemas import DemandRecord
from inventory.schemas import InventoryRecord
from replenishment.schemas import ReplenishmentInput

from decision_coordinator.schemas import DecisionCoordinatorInput

from simulation_engine.schemas import SimulationInput
from simulation_engine.service import run_simulation
from simulation_engine.scenarios import (
    build_baseline_scenario,
    build_demand_spike_scenario,
    build_supplier_delay_scenario,
)

from scenario_analysis.service import ScenarioAnalysisService

from tools.schemas import (
    ForecastToolInput,
    InventoryStatusToolInput,
    ReplenishmentToolInput,
)


class DummyForecastModel:
    """
    Minimal forecast model used only for smoke testing.
    """

    def predict(self, rows):
        return [15.0 for _ in rows]


def build_mock_coordinator_input() -> DecisionCoordinatorInput:
    """
    Build a minimal but realistic supply chain state.
    """

    sku_id = "SKU_1"
    location_id = "LOC_1"

    series_records = [
        DemandRecord(sku_id, location_id, date(2026, 3, 1), 12.0),
        DemandRecord(sku_id, location_id, date(2026, 3, 2), 14.0),
        DemandRecord(sku_id, location_id, date(2026, 3, 3), 13.0),
        DemandRecord(sku_id, location_id, date(2026, 3, 4), 15.0),
        DemandRecord(sku_id, location_id, date(2026, 3, 5), 14.0),
    ]

    forecast_input = ForecastToolInput(
        model=DummyForecastModel(),
        series_records=series_records,
        horizon=3,
    )

    inventory_record = InventoryRecord(
        sku_id=sku_id,
        location_id=location_id,
        on_hand=25.0,
        on_order=0.0,
        reserved=5.0,
    )

    inventory_input = InventoryStatusToolInput(
        record=inventory_record,
        expected_daily_demand=15.0,
        lead_time_days=5,
    )

    replenishment_input = ReplenishmentToolInput(
        replenishment_input=ReplenishmentInput(
            sku_id=sku_id,
            location_id=location_id,
            inventory_position=20.0,
            expected_daily_demand=15.0,
            lead_time_days=5,
            safety_stock=20.0,
        )
    )

    return DecisionCoordinatorInput(
        forecast_input=forecast_input,
        inventory_input=inventory_input,
        replenishment_input=replenishment_input,
    )


def main() -> None:
    baseline_input = build_mock_coordinator_input()

    scenarios = [
        build_baseline_scenario(),
        build_demand_spike_scenario(multiplier=1.5),
        build_supplier_delay_scenario(multiplier=2.0),
    ]

    simulation_input = SimulationInput(
        baseline_input=baseline_input,
        scenarios=scenarios,
    )

    simulation_result = run_simulation(simulation_input)

    analysis_service = ScenarioAnalysisService()
    analysis_result = analysis_service.analyze(simulation_result)

    print("\nScenario analysis completed.")
    print(f"Baseline scenario: {analysis_result.baseline_scenario_name}")
    print("Number of comparison rows:", len(analysis_result.comparison_rows))
    print()

    print(
        f"{'Scenario':<18}"
        f"{'Reorder':<10}"
        f"{'Units':<12}"
        f"{'Delta_vs_Baseline':<20}"
    )

    for row in analysis_result.comparison_rows:
        print(
            f"{row.scenario_name:<18}"
            f"{str(row.reorder):<10}"
            f"{row.recommended_units:<12.1f}"
            f"{row.delta_vs_baseline:<20.1f}"
        )


if __name__ == "__main__":
    main()