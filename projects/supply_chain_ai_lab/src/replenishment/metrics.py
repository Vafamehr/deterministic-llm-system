
from .schemas import (
    ReplenishmentInput,
    ReorderPointResult,
    ReorderDecisionResult,
    OrderQuantityResult,
    ReplenishmentRecommendation,
)


def compute_lead_time_demand(replenishment_input: ReplenishmentInput) -> float:
    """
    Compute expected demand during lead time.
    """

    if replenishment_input.expected_daily_demand < 0:
        raise ValueError("expected_daily_demand cannot be negative.")

    if replenishment_input.lead_time_days < 0:
        raise ValueError("lead_time_days cannot be negative.")

    return float(
        replenishment_input.expected_daily_demand * replenishment_input.lead_time_days
    )


def compute_reorder_point(
    replenishment_input: ReplenishmentInput,
) -> ReorderPointResult:
    """
    Compute reorder point.

    reorder_point = lead_time_demand + safety_stock
    """

    if replenishment_input.safety_stock < 0:
        raise ValueError("safety_stock cannot be negative.")

    lead_time_demand = compute_lead_time_demand(replenishment_input)
    reorder_point = lead_time_demand + replenishment_input.safety_stock

    return ReorderPointResult(
        sku_id=replenishment_input.sku_id,
        location_id=replenishment_input.location_id,
        reorder_point=float(reorder_point),
    )


def compute_reorder_decision(
    replenishment_input: ReplenishmentInput,
) -> ReorderDecisionResult:
    """
    Decide whether replenishment is needed.

    Reorder when inventory_position is below reorder_point.
    """

    reorder_point_result = compute_reorder_point(replenishment_input)

    should_reorder = (
        replenishment_input.inventory_position < reorder_point_result.reorder_point
    )

    return ReorderDecisionResult(
        sku_id=replenishment_input.sku_id,
        location_id=replenishment_input.location_id,
        should_reorder=should_reorder,
    )


def compute_order_quantity(
    replenishment_input: ReplenishmentInput,
) -> OrderQuantityResult:
    """
    Compute a simple order quantity.

    First version policy:
    if reorder is needed, order enough to raise inventory position
    up to the reorder point.
    """

    reorder_point_result = compute_reorder_point(replenishment_input)
    reorder_decision_result = compute_reorder_decision(replenishment_input)

    if not reorder_decision_result.should_reorder:
        order_quantity = 0.0
    else:
        gap = reorder_point_result.reorder_point - replenishment_input.inventory_position
        order_quantity = max(0.0, float(gap))

    return OrderQuantityResult(
        sku_id=replenishment_input.sku_id,
        location_id=replenishment_input.location_id,
        order_quantity=order_quantity,
    )


def get_replenishment_recommendation(
    replenishment_input: ReplenishmentInput,
) -> ReplenishmentRecommendation:
    """
    Return a full structured replenishment recommendation.
    """

    reorder_point_result = compute_reorder_point(replenishment_input)
    reorder_decision_result = compute_reorder_decision(replenishment_input)
    order_quantity_result = compute_order_quantity(replenishment_input)

    return ReplenishmentRecommendation(
        sku_id=replenishment_input.sku_id,
        location_id=replenishment_input.location_id,
        reorder_point=reorder_point_result.reorder_point,
        should_reorder=reorder_decision_result.should_reorder,
        order_quantity=order_quantity_result.order_quantity,
    )