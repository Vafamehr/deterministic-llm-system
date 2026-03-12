from __future__ import annotations

from replenishment.service import get_replenishment_recommendation
from replenishment.schemas import ReplenishmentInput, ReplenishmentRecommendation

from .schemas import ReplenishmentToolInput, ReplenishmentToolOutput


def get_replenishment_recommendation_tool(
    input_data: ReplenishmentToolInput,
) -> ReplenishmentToolOutput:
    """
    Tool wrapper for the replenishment subsystem.

    This tool delegates to the replenishment service layer and
    returns a structured recommendation for higher-level decision flows.
    """

    replenishment_input: ReplenishmentInput = input_data.replenishment_input

    recommendation: ReplenishmentRecommendation = get_replenishment_recommendation(
        replenishment_input
    )

    reason_codes = []

    if recommendation.should_reorder:
        reason_codes.append("inventory_below_reorder_point")

    return ReplenishmentToolOutput(
        sku_id=recommendation.sku_id,
        location_id=recommendation.location_id,
        reorder_point=recommendation.reorder_point,
        should_reorder=recommendation.should_reorder,
        recommended_order_units=recommendation.order_quantity,
        reason_codes=reason_codes,
    )