from dataclasses import dataclass
from typing import List, Any

from tools.schemas import (
    ForecastToolInput,
    ForecastToolOutput,
    InventoryStatusToolInput,
    InventoryStatusToolOutput,
    ReplenishmentToolInput,
    ReplenishmentToolOutput,
)


@dataclass
class DecisionCoordinatorInput:
    """
    Input to the Decision Coordinator.

    This object bundles the inputs required for each tool that participates
    in the end-to-end supply chain decision flow.

    The coordinator does not transform domain data itself. It simply forwards
    the appropriate inputs to the tool runner.
    """

    forecast_input: ForecastToolInput
    inventory_input: InventoryStatusToolInput
    replenishment_input: ReplenishmentToolInput


@dataclass
class DecisionStepTrace:
    """
    Trace record for a single step in the decision pipeline.

    This enables visibility into the decision execution order
    and will later support debugging, simulation analysis,
    and agent reasoning.
    """

    step_name: str
    tool_name: str
    input_data: Any
    output_data: Any


@dataclass
class DecisionCoordinatorResult:
    """
    Final result of the supply chain decision pipeline.

    This bundles the outputs of all executed tools and provides
    a trace of the steps executed by the coordinator.
    """

    forecast_result: ForecastToolOutput
    inventory_result: InventoryStatusToolOutput
    replenishment_result: ReplenishmentToolOutput
    execution_trace: List[DecisionStepTrace]