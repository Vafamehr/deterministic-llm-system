from dataclasses import dataclass


@dataclass
class ReplenishmentInput:
    """
    Input required to compute replenishment decisions
    for a single SKU-location pair.
    """

    sku_id: str
    location_id: str

    inventory_position: float
    expected_daily_demand: float

    lead_time_days: int
    safety_stock: float


@dataclass
class ReorderPointResult:
    """
    Represents the computed reorder point.
    """

    sku_id: str
    location_id: str
    reorder_point: float


@dataclass
class ReorderDecisionResult:
    """
    Represents whether a reorder should occur.
    """

    sku_id: str
    location_id: str
    should_reorder: bool


@dataclass
class OrderQuantityResult:
    """
    Represents a suggested order quantity.
    """

    sku_id: str
    location_id: str
    order_quantity: float


@dataclass
class ReplenishmentRecommendation:
    """
    Full replenishment recommendation.
    """

    sku_id: str
    location_id: str

    reorder_point: float
    should_reorder: bool
    order_quantity: float