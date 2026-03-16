from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DisruptionType(Enum): # considered only these options as disruptions for now. 
    SUPPLIER_DELAY = "supplier_delay"
    DEMAND_SURGE = "demand_surge"
    WAREHOUSE_DISRUPTION = "warehouse_disruption"
    INVENTORY_LOSS = "inventory_loss"
    TRANSPORTATION_DELAY = "transportation_delay"


class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class AffectedNode:
    node_id: str
    node_type: str  # supplier, warehouse, store, lane, region


@dataclass(frozen=True)
class DisruptionEvent:
    event_id: str
    disruption_type: DisruptionType
    severity: SeverityLevel
    duration_days: int
    affected_node: AffectedNode
    start_day: int = 0
    description: Optional[str] = None


@dataclass(frozen=True)
class DisruptionImpact:
    supplier_delay_days: int = 0
    demand_multiplier: float = 1.0
    inventory_loss_units: float = 0.0
    warehouse_capacity_multiplier: float = 1.0
    transportation_delay_days: int = 0


@dataclass(frozen=True)
class DisruptionScenario:
    scenario_name: str
    event: DisruptionEvent
    impact: DisruptionImpact