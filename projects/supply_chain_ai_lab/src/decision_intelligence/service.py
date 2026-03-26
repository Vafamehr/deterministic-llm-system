from __future__ import annotations

from decision_intelligence.schemas import (
    DecisionIntelligenceOutput,
    InventoryState,
    KeyRisk,
)


def _is_high_stockout_risk(stockout_risk: object) -> bool:
    if isinstance(stockout_risk, bool):
        return stockout_risk

    if isinstance(stockout_risk, str):
        normalized = stockout_risk.strip().upper()
        return normalized in {"HIGH", "TRUE", "YES"}

    return False


def classify_decision_intelligence(
    days_of_supply: float,
    stockout_risk: object,
    inventory_pressure: str,
    overstock_risk: str,
) -> DecisionIntelligenceOutput:
    """
    Convert interpreted scenario-analysis signals into a deterministic
    business-readable state classification.

    Inputs are existing signals only.
    This layer does not compute raw inventory metrics.
    """
    stockout_high = _is_high_stockout_risk(stockout_risk)
    pressure = inventory_pressure.strip().upper()
    overstock = overstock_risk.strip().upper()

    if overstock == "HIGH":
        return DecisionIntelligenceOutput(
            inventory_state=InventoryState.OVERSTOCK,
            key_risk=KeyRisk.EXCESS_RISK,
            reasoning_summary=(
                "High days of supply indicates excess inventory exposure."
            ),
        )

    if pressure == "HIGH":
        return DecisionIntelligenceOutput(
            inventory_state=InventoryState.UNDERSTOCK,
            key_risk=KeyRisk.SHORTAGE_RISK,
            reasoning_summary=(
                "Low days of supply and high replenishment urgency indicate an understock condition."
            ),
        )

    if stockout_high:
        return DecisionIntelligenceOutput(
            inventory_state=InventoryState.BALANCED,
            key_risk=KeyRisk.HIDDEN_RISK,
            reasoning_summary=(
                "Inventory appears balanced, but stockout risk remains elevated."
            ),
        )

    return DecisionIntelligenceOutput(
        inventory_state=InventoryState.BALANCED,
        key_risk=KeyRisk.STABLE,
        reasoning_summary=(
            "Inventory coverage and risk signals indicate a stable condition."
        ),
    )