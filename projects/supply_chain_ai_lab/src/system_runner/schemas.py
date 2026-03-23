from dataclasses import dataclass
from typing import Optional

from decision_coordinator.schemas import (
    DecisionCoordinatorInput,
    DecisionCoordinatorResult,
)

from disruption_modeling.service import ResolvedDisruption
from disruption_modeling.schemas import DisruptionScenario

from allocation.schemas import AllocationRequest, AllocationResult

from simulation_engine.schemas import SimulationInput, SimulationResult
from network_monitoring.schemas import NetworkHealthReport


@dataclass
class SystemRunnerConfig:
    mode: str  # "baseline", "disruption", "allocation", "simulation", "monitoring"


@dataclass
class SystemRunnerInput:
    decision_input: DecisionCoordinatorInput
    disruption_scenario: Optional[DisruptionScenario] = None
    simulation_input: Optional[SimulationInput] = None
    allocation_request: Optional[AllocationRequest] = None


@dataclass
class SystemRunnerResult:
    core_result: Optional[DecisionCoordinatorResult] = None
    disruption_result: Optional[ResolvedDisruption] = None
    allocation_result: Optional[AllocationResult] = None
    simulation_result: Optional[SimulationResult] = None
    monitoring_result: Optional[NetworkHealthReport] = None