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

    # --- Step 2: Inventory ---
    inventory_output: InventoryStatusToolOutput = run_tool(
        "inventory_status",
        decision_input.inventory_input,
    )

    execution_trace.append(
        DecisionStepTrace(
            step_name="evaluate_inventory",
            tool_name="inventory_status",
            input_data=decision_input.inventory_input,
            output_data=inventory_output,
        )
    )

    # --- Step 3: Replenishment ---
    replenishment_output: ReplenishmentToolOutput = run_tool(
        "replenishment",
        decision_input.replenishment_input,
    )

    execution_trace.append(
        DecisionStepTrace(
            step_name="generate_replenishment",
            tool_name="replenishment",
            input_data=decision_input.replenishment_input,
            output_data=replenishment_output,
        )
    )

    return DecisionCoordinatorResult(
        forecast_result=forecast_output,
        inventory_result=inventory_output,
        replenishment_result=replenishment_output,
        execution_trace=execution_trace,
    )