"""
Smoke test for the Simulation Engine.

This test builds a small mock supply chain world and runs the
simulation engine against multiple scenarios.

The goal is to verify:

simulation → decision coordinator → tools

works end-to-end.
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

    # Historical demand
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

    # Inventory intentionally tight
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


def main():

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

    result = run_simulation(simulation_input)

    print("\nSimulation completed.")
    print("Number of scenario results:", len(result.scenario_results))
    print()

    for scenario_result in result.scenario_results:

        replenishment = scenario_result.decision_result.replenishment_result

        print(
            f"{scenario_result.scenario.name:15} "
            f"reorder={replenishment.should_reorder} "
            f"recommended_units={replenishment.recommended_order_units}"
        )


if __name__ == "__main__":
    main()