from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class NetworkInventoryRecord:
    sku_id: str
    location_id: str
    on_hand: float
    expected_daily_demand: float


@dataclass(frozen=True)
class StockoutRisk:
    sku_id: str
    location_id: str
    days_of_supply: float


@dataclass(frozen=True)
class NetworkHealthReport:
    stockout_risks: List[StockoutRisk]