from __future__ import annotations

from inventory.service import (
    get_inventory_position,
    get_days_of_supply,
    get_stockout_risk,
)
from inventory.schemas import InventoryRecord

from .schemas import InventoryStatusToolInput, InventoryStatusToolOutput


def get_inventory_status(input_data: InventoryStatusToolInput) -> InventoryStatusToolOutput:
    """
    Tool wrapper for the inventory subsystem.

    This tool aggregates several inventory service calls into a single
    operational inventory status response.
    """

    record: InventoryRecord = input_data.record

    position_result = get_inventory_position(record)

    dos_result = get_days_of_supply(
        record,
        expected_daily_demand=input_data.expected_daily_demand,
    )

    risk_result = get_stockout_risk(
        record,
        expected_daily_demand=input_data.expected_daily_demand,
        lead_time_days=input_data.lead_time_days,
    )

    return InventoryStatusToolOutput(
        sku_id=record.sku_id,
        location_id=record.location_id,
        inventory_position=position_result.inventory_position,
        days_of_supply=dos_result.days_of_supply,
        stockout_risk="HIGH" if risk_result.stockout_risk else "LOW",
    )