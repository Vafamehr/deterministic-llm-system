from inventory.schemas import InventoryRecord
from replenishment.schemas import ReplenishmentInput

from tools.runner import run_tool
from tools.schemas import (
    InventoryStatusToolInput,
    ReplenishmentToolInput,
)


def run_inventory_smoke_test():
    inventory_input = InventoryStatusToolInput(
        record=InventoryRecord(
            sku_id="SKU_001",
            location_id="LOC_001",
            on_hand=100.0,
            on_order=25.0,
            reserved=10.0,
        ),
        expected_daily_demand=15.0,
        lead_time_days=5,
    )

    result = run_tool("inventory_status", inventory_input)

    print("INVENTORY RESULT")
    print(result)
    print()


def run_replenishment_smoke_test():
    replenishment_input = ReplenishmentToolInput(
        replenishment_input=ReplenishmentInput(
            sku_id="SKU_001",
            location_id="LOC_001",
            inventory_position=115.0,
            expected_daily_demand=15.0,
            lead_time_days=5,
            safety_stock=20.0,
        )
    )

    result = run_tool("replenishment", replenishment_input)

    print("REPLENISHMENT RESULT")
    print(result)
    print()


if __name__ == "__main__":
    run_inventory_smoke_test()
    run_replenishment_smoke_test()