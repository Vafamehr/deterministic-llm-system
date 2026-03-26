from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class InventoryState(str, Enum):
    UNDERSTOCK = "UNDERSTOCK"
    BALANCED = "BALANCED"
    OVERSTOCK = "OVERSTOCK"


class KeyRisk(str, Enum):
    SHORTAGE_RISK = "SHORTAGE_RISK"
    EXCESS_RISK = "EXCESS_RISK"
    HIDDEN_RISK = "HIDDEN_RISK"
    STABLE = "STABLE"


@dataclass(frozen=True)
class DecisionIntelligenceOutput:
    inventory_state: InventoryState
    key_risk: KeyRisk
    reasoning_summary: str