from dataclasses import dataclass


@dataclass
class ReplenishmentInput:
    sku_id: str
    location_id: str

    inventory_position: float
    expected_daily_demand: float

    lead_time_days: int
    safety_stock: float


@dataclass
class ReorderPointResult:
    sku_id: str
    location_id: str
    reorder_point: float


@dataclass
class ReorderDecisionResult:
    sku_id: str
    location_id: str
    should_reorder: bool


@dataclass
class OrderQuantityResult:
    sku_id: str
    location_id: str
    order_quantity: float


@dataclass
class ReplenishmentRecommendation:
    sku_id: str
    location_id: str

    reorder_point: float
    should_reorder: bool
    order_quantity: float