# projects/supply_chain_ai_lab/src/replenishment/smoke_test.py

from .schemas import ReplenishmentInput
from .service import (
    get_order_quantity,
    get_reorder_point,
    get_replenishment_recommendation,
    should_reorder,
)


def run_smoke_test() -> None:


    replenishment_input = ReplenishmentInput(
    sku_id="SKU_001",
    location_id="STORE_001",
    inventory_position=40.0,
    expected_daily_demand=12.0,
    lead_time_days=5,
    safety_stock=20.0,
)

    reorder_point_result = get_reorder_point(replenishment_input)
    reorder_decision_result = should_reorder(replenishment_input)
    order_quantity_result = get_order_quantity(replenishment_input)
    recommendation = get_replenishment_recommendation(replenishment_input)

    print("=== REORDER POINT RESULT ===")
    print(reorder_point_result)

    print("\n=== REORDER DECISION RESULT ===")
    print(reorder_decision_result)

    print("\n=== ORDER QUANTITY RESULT ===")
    print(order_quantity_result)

    print("\n=== FULL REPLENISHMENT RECOMMENDATION ===")
    print(recommendation)


if __name__ == "__main__":
    
    run_smoke_test()