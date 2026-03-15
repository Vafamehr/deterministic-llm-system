"""
Smoke test for the Simulation Engine.

This test runs a minimal simulation using simple mock inputs.
The goal is to verify that the simulation engine can call the
decision coordinator and execute scenario runs without import or
basic schema-construction errors.
"""

from datetime import date

from demand_forecasting.schemas import DemandRecord
from replenishment.schemas import ReplenishmentInput
from decision_coordinator.schemas import DecisionCoordinatorInput
from simulation_engine.schemas import SimulationInput
from simulation_engine.scenarios import (
    build_baseline_scenario,
    build_demand_spike_scenario,
    build_supplier_delay_scenario,
)
from simulation_engine.service import run_simulation
from tools.schemas import (
    ForecastToolInput,
    InventoryStatusToolInput,
    ReplenishmentToolInput,
)
from inventory.schemas import InventoryRecord


class DummyForecastModel:
    """
    Minimal forecast model for smoke testing.
    Returns a constant prediction for each requested row.
    """

    def predict(self, rows):
        return [12.0 for _ in rows]


def build_mock_coordinator_input() -> DecisionCoordinatorInput:
    """
    Build a minimal DecisionCoordinatorInput using the real tool schemas.
    """

    sku_id = "SKU_1"
    location_id = "LOC_1"

    series_records = [
        DemandRecord(sku_id=sku_id, location_id=location_id, date=date(2026, 3, 1), demand=10.0),
        DemandRecord(sku_id=sku_id, location_id=location_id, date=date(2026, 3, 2), demand=12.0),
        DemandRecord(sku_id=sku_id, location_id=location_id, date=date(2026, 3, 3), demand=11.0),
        DemandRecord(sku_id=sku_id, location_id=location_id, date=date(2026, 3, 4), demand=13.0),
        DemandRecord(sku_id=sku_id, location_id=location_id, date=date(2026, 3, 5), demand=12.0),
    ]

    forecast_input = ForecastToolInput(
        model=DummyForecastModel(),
        series_records=series_records,
        horizon=3,
    )

    inventory_record = InventoryRecord(
        sku_id=sku_id,
        location_id=location_id,
        on_hand=80.0,
        on_order=20.0,
        reserved=5.0,
    )

    inventory_input = InventoryStatusToolInput(
        record=inventory_record,
        expected_daily_demand=12.0,
        lead_time_days=5,
    )

    replenishment_input = ReplenishmentToolInput(
        replenishment_input=ReplenishmentInput(
            sku_id=sku_id,
            location_id=location_id,
            inventory_position=95.0,
            expected_daily_demand=12.0,
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
        build_demand_spike_scenario(),
        build_supplier_delay_scenario(),
    ]

    simulation_input = SimulationInput(
        baseline_input=baseline_input,
        scenarios=scenarios,
    )

    result = run_simulation(simulation_input)

    print("Simulation completed.")
    print("Number of scenario results:", len(result.scenario_results))

    for scenario_result in result.scenario_results:
        print(
            f"- {scenario_result.scenario.name}: "
            f"reorder={scenario_result.decision_result.replenishment_result.should_reorder}, "
            f"recommended_units={scenario_result.decision_result.replenishment_result.recommended_order_units}"
        )


if __name__ == "__main__":
    main()