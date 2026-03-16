from dataclasses import dataclass
from typing import List


@dataclass
class ProductRecord:
    sku_id: str
    name: str
    category: str
    unit_cost: float


@dataclass
class LocationRecord:
    location_id: str
    name: str
    type: str
    region: str


@dataclass
class SupplierRecord:
    supplier_id: str
    name: str
    region: str


@dataclass
class TransportationLaneRecord:
    supplier_id: str
    location_id: str
    lead_time_days: int
    transport_cost: float




@dataclass
class SampleNetwork:
    products: List[ProductRecord]
    locations: List[LocationRecord]
    suppliers: List[SupplierRecord]
    lanes: List[TransportationLaneRecord]
    inventory: List