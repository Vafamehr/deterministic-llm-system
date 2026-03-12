from datetime import date

from decision_coordinator.schemas import DecisionCoordinatorInput
from decision_coordinator.service import run_supply_chain_decision

from demand_forecasting.schemas import DemandRecord
from inventory.schemas import InventoryRecord
from replenishment.schemas import ReplenishmentInput

from tools.schemas import (
    ForecastToolInput,
    InventoryStatusToolInput,
    ReplenishmentToolInput,
)


class DummyForecastModel:
    """
    Minimal stub model used only for the smoke test.
    The real forecasting system expects a model with .predict().
    """

    def predict(self, X):
        return [23.0] * len(X)


def run_decision_coordinator_smoke_test() -> None:
    series_records = [
        DemandRecord("sku_1", "loc_1", date(2024, 1, 1), 20.0),
        DemandRecord("sku_1", "loc_1", date(2024, 1, 2), 22.0),
        DemandRecord("sku_1", "loc_1", date(2024, 1, 3), 21.0),
        DemandRecord("sku_1", "loc_1", date(2024, 1, 4), 24.0),
        DemandRecord("sku_1", "loc_1", date(2024, 1, 5), 23.0),
        DemandRecord("sku_1", "loc_1", date(2024, 1, 6), 25.0),
    ]

    inventory_record = InventoryRecord(
        sku_id="sku_1",
        location_id="loc_1",
        on_hand=40.0,
        on_order=15.0,
        reserved=5.0,
    )

    replenishment_input = ReplenishmentInput(
        sku_id="sku_1",
        location_id="loc_1",
        inventory_position=50.0,
        expected_daily_demand=23.0,
        lead_time_days=5,
        safety_stock=20.0,
    )

    decision_input = DecisionCoordinatorInput(
        forecast_input=ForecastToolInput(
            model=DummyForecastModel(),
            series_records=series_records,
            horizon=3,
        ),
        inventory_input=InventoryStatusToolInput(
            record=inventory_record,
            expected_daily_demand=23.0,
            lead_time_days=5,
        ),
        replenishment_input=ReplenishmentToolInput(
            replenishment_input=replenishment_input,
        ),
    )

    result = run_supply_chain_decision(decision_input)

    assert result.forecast_result is not None
    assert result.inventory_result is not None
    assert result.replenishment_result is not None
    assert len(result.execution_trace) == 3

    assert result.execution_trace[0].tool_name == "forecast"
    assert result.execution_trace[1].tool_name == "inventory_status"
    assert result.execution_trace[2].tool_name == "replenishment"

    print("Decision Coordinator smoke test passed.")


if __name__ == "__main__":
    run_decision_coordinator_smoke_test()