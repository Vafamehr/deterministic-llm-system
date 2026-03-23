""" 
For now keeps modules loosely coupled,-------->
reality: forecast → influences inventory expectations
inventory → influences replenishment quantity
TODO: later
"""

from tools.runner import run_tool

from .schemas import (
    DecisionCoordinatorInput,
    DecisionCoordinatorResult,
    DecisionStepTrace,
)

from tools.schemas import (
    ForecastToolOutput,
    InventoryStatusToolOutput,
    ReplenishmentToolOutput,
)


def run_supply_chain_decision(
    decision_input: DecisionCoordinatorInput
) -> DecisionCoordinatorResult:
    """
    Executes the full supply chain decision flow.

    Pipeline:

    forecast
        ↓
    inventory evaluation
        ↓
    replenishment recommendation
    """

    execution_trace = []

    # --- Step 1: Forecast ---
    forecast_output: ForecastToolOutput = run_tool(
        "forecast",
        decision_input.forecast_input,
    )

    execution_trace.append(
        DecisionStepTrace(
            step_name="forecast_demand",
            tool_name="forecast",
            input_data=decision_input.forecast_input,
            output_data=forecast_output,
        )
    )


    predicted_values = forecast_output.predicted_values
    expected_daily_demand = sum(predicted_values) / len(predicted_values)

    impact = getattr(decision_input, "disruption_impact", None)
    if impact:
        expected_daily_demand *= impact.demand_multiplier

    if decision_input.demand_multiplier_override is not None:
        expected_daily_demand *= decision_input.demand_multiplier_override

    # --- Step 2: Inventory ---
    updated_inventory_input = type(decision_input.inventory_input)(
        record=decision_input.inventory_input.record,
        expected_daily_demand=expected_daily_demand,
        lead_time_days=decision_input.inventory_input.lead_time_days,
    )

    inventory_output: InventoryStatusToolOutput = run_tool(
        "inventory_status",
        updated_inventory_input,
    )

    execution_trace.append(
        DecisionStepTrace(
            step_name="evaluate_inventory",
            tool_name="inventory_status",
            input_data=updated_inventory_input,
            output_data=inventory_output,
        )
    )

    # --- Step 3: Replenishment ---

    rep_input = decision_input.replenishment_input.replenishment_input

    updated_rep_input = type(rep_input)(
        sku_id=rep_input.sku_id,
        location_id=rep_input.location_id,
        inventory_position=inventory_output.inventory_position,
        expected_daily_demand=expected_daily_demand,
        lead_time_days=rep_input.lead_time_days,
        safety_stock=rep_input.safety_stock,
    )

    updated_replenishment_tool_input = type(decision_input.replenishment_input)(
        replenishment_input=updated_rep_input
    )

    replenishment_output: ReplenishmentToolOutput = run_tool(
        "replenishment",
        updated_replenishment_tool_input,
    )

    execution_trace.append(
        DecisionStepTrace(
            step_name="generate_replenishment",
            tool_name="replenishment",
            input_data=updated_replenishment_tool_input,
            output_data=replenishment_output,
        )
    )

    return DecisionCoordinatorResult(
        forecast_result=forecast_output,
        inventory_result=inventory_output,
        replenishment_result=replenishment_output,
        execution_trace=execution_trace,
    )