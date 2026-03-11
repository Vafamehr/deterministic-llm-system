from .schemas import InventoryRecord
from .metrics import (
    compute_inventory_position,
    compute_days_of_supply,
    assess_stockout_risk,
)


def get_inventory_position(record: InventoryRecord):
    """
    Public service to compute inventory position.
    """

    return compute_inventory_position(record)


def get_days_of_supply(record: InventoryRecord, expected_daily_demand: float):
    """
    Public service to compute days of supply.
    """

    return compute_days_of_supply(record, expected_daily_demand)


def get_stockout_risk(
    record: InventoryRecord,
    expected_daily_demand: float,
    lead_time_days: int,
):
    """
    Public service to assess stockout risk.
    """

    return assess_stockout_risk(
        record,
        expected_daily_demand,
        lead_time_days,
    )