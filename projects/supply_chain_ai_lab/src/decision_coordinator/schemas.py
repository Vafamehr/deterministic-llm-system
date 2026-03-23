from dataclasses import dataclass
from typing import Any, List, Optional

from disruption_modeling.schemas import DisruptionImpact

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
    """

    forecast_input: ForecastToolInput
    inventory_input: InventoryStatusToolInput
    replenishment_input: ReplenishmentToolInput
    disruption_impact: Optional[DisruptionImpact] = None
    demand_multiplier_override: Optional[float] = None


@dataclass
class DecisionStepTrace:
    """
    Trace record for a single step in the decision pipeline.
    """

    step_name: str
    tool_name: str
    input_data: Any
    output_data: Any


@dataclass
class DecisionCoordinatorResult:
    """
    Final result of the supply chain decision pipeline.
    """

    forecast_result: ForecastToolOutput
    inventory_result: InventoryStatusToolOutput
    replenishment_result: ReplenishmentToolOutput
    execution_trace: List[DecisionStepTrace]