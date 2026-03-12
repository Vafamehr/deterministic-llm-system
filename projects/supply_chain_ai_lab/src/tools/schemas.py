from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, List, Optional
from replenishment.schemas import ReplenishmentInput


# -------------------------------------------------------------------
# Forecast Tool
# -------------------------------------------------------------------

@dataclass(frozen=True)
class ForecastToolInput:
    """
    Input contract for the forecasting tool.

    This reflects the current forecasting subsystem as implemented today:
    a trained model plus the historical records for one SKU-location series.
    """
    model: Any
    series_records: List[Any]
    horizon: int = 1


@dataclass(frozen=True)
class ForecastToolOutput:
    """
    Output contract for the forecasting tool.
    """
    sku_id: str
    location_id: str
    horizon: int
    predicted_values: List[float]
    model_name: str
    generated_for_date: Optional[date] = None


# -------------------------------------------------------------------
# Inventory Status Tool
# -------------------------------------------------------------------

@dataclass(frozen=True)
class InventoryStatusToolInput:
    """
    Input contract for the inventory status tool.

    The tool wraps the inventory service layer and computes:
    - inventory position
    - days of supply
    - stockout risk
    """
    record: Any
    expected_daily_demand: float
    lead_time_days: int


@dataclass(frozen=True)
class InventoryStatusToolOutput:
    """
    Output contract for the inventory status tool.
    """
    sku_id: str
    location_id: str
    inventory_position: float
    days_of_supply: Optional[float]
    stockout_risk: str


# -------------------------------------------------------------------
# Replenishment Recommendation Tool
# -------------------------------------------------------------------

@dataclass(frozen=True)
class ReplenishmentToolInput:
    """
    Input contract for the replenishment recommendation tool.
    """
    replenishment_input: ReplenishmentInput
    

@dataclass(frozen=True)
class ReplenishmentToolOutput:
    """
    Output contract for the replenishment recommendation tool.
    """
    sku_id: str
    location_id: str
    reorder_point: float
    should_reorder: bool
    recommended_order_units: float
    reason_codes: List[str]