from .schemas import (
    InventoryRecord,
    InventoryPositionResult,
    DaysOfSupplyResult,
    StockRiskResult,
)


def compute_inventory_position(record: InventoryRecord) -> InventoryPositionResult:
    """
    Computes inventory position.

    inventory_position = on_hand + on_order - reserved
    """

    inventory_position = record.on_hand + record.on_order - record.reserved

    return InventoryPositionResult(
        sku_id=record.sku_id,
        location_id=record.location_id,
        inventory_position=float(inventory_position),
    )


def compute_days_of_supply(
    record: InventoryRecord,
    expected_daily_demand: float,
) -> DaysOfSupplyResult:
    """
    Computes days of supply.

    days_of_supply = on_hand / expected_daily_demand
    """

    if expected_daily_demand <= 0:
        raise ValueError("expected_daily_demand must be positive")

    days_of_supply = record.on_hand / expected_daily_demand

    return DaysOfSupplyResult(
        sku_id=record.sku_id,
        location_id=record.location_id,
        days_of_supply=float(days_of_supply),
    )


def assess_stockout_risk(
    record: InventoryRecord,
    expected_daily_demand: float,
    lead_time_days: int,
) -> StockRiskResult:
    """
    Simple stockout risk check.

    If on-hand inventory will run out before replenishment lead time,
    we flag a stockout risk.
    """

    if expected_daily_demand <= 0:
        raise ValueError("expected_daily_demand must be positive")

    days_of_supply = record.on_hand / expected_daily_demand

    stockout_risk = days_of_supply < lead_time_days

    return StockRiskResult(
        sku_id=record.sku_id,
        location_id=record.location_id,
        stockout_risk=stockout_risk,
    )