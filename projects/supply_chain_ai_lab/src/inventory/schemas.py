from dataclasses import dataclass


@dataclass
class InventoryRecord:
    """
    Represents the inventory state for one SKU at one location.
    """

    sku_id: str
    location_id: str

    on_hand: float
    on_order: float
    reserved: float = 0.0


@dataclass
class InventoryPositionResult:
    """
    Represents computed inventory position.
    """

    sku_id: str
    location_id: str
    inventory_position: float


@dataclass
class DaysOfSupplyResult:
    """
    Represents the estimated number of days inventory will last.
    """

    sku_id: str
    location_id: str
    days_of_supply: float


@dataclass
class StockRiskResult:
    """
    Represents a simple stock risk signal.
    """

    sku_id: str
    location_id: str
    stockout_risk: bool