from dataclasses import dataclass
from typing import Optional

from decision_coordinator.schemas import (
    DecisionCoordinatorInput,
    DecisionCoordinatorResult,
)

from disruption_modeling.service import ResolvedDisruption
from disruption_modeling.schemas import DisruptionScenario


@dataclass
class SystemRunnerConfig:
    mode: str  # "baseline", "disruption", "allocation", "simulation", "monitoring"


@dataclass
class SystemRunnerInput:
    decision_input: DecisionCoordinatorInput
    disruption_scenario: Optional[DisruptionScenario] = None


@dataclass
class SystemRunnerResult:
    core_result: DecisionCoordinatorResult
    disruption_result: Optional[ResolvedDisruption] = None
    allocation_result: Optional[object] = None
    simulation_result: Optional[object] = None
    monitoring_result: Optional[object] = None