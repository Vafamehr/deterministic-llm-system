# projects/supply_chain_ai_lab/src/replenishment/service.py

from .metrics import (
    compute_order_quantity,
    compute_reorder_decision,
    compute_reorder_point,
    get_replenishment_recommendation as build_replenishment_recommendation,
)
from .schemas import (
    ReorderDecisionResult,
    ReorderPointResult,
    ReplenishmentInput,
    ReplenishmentRecommendation,
    OrderQuantityResult,
)


def get_reorder_point(replenishment_input: ReplenishmentInput) -> ReorderPointResult:
    """
    Service entry point for reorder point calculation.
    """
    return compute_reorder_point(replenishment_input)


def should_reorder(replenishment_input: ReplenishmentInput) -> ReorderDecisionResult:
    """
    Service entry point for reorder decision calculation.
    """
    return compute_reorder_decision(replenishment_input)


def get_order_quantity(
    replenishment_input: ReplenishmentInput,
) -> OrderQuantityResult:
    """
    Service entry point for order quantity calculation.
    """
    return compute_order_quantity(replenishment_input)


def get_replenishment_recommendation(
    replenishment_input: ReplenishmentInput,
) -> ReplenishmentRecommendation:
    """
    Service entry point for full replenishment recommendation.
    """
    return build_replenishment_recommendation(replenishment_input)