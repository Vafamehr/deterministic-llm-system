from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True) # deisred demand of each store 
class LocationDemand:
    location_id: str
    demand_units: float


@dataclass(frozen=True)
class AllocationRequest: # The problem, how to dedicate limited inventory among abundant demands of stores
    sku_id: str
    available_inventory: float
    location_demands: List[LocationDemand]


@dataclass(frozen=True)  # Represents the decision for one location: location can be DC,fulfillment nodes, store etc 
class LocationAllocation:
    location_id: str
    allocated_units: float


@dataclass(frozen=True)
class AllocationResult:
    sku_id: str
    allocations: List[LocationAllocation]