from dataclasses import dataclass
from typing import Optional

from allocation.schemas import AllocationRequest, AllocationResult
from decision_coordinator.schemas import (
    DecisionCoordinatorInput,
    DecisionCoordinatorResult,
)
from disruption_modeling.schemas import DisruptionScenario
from disruption_modeling.service import ResolvedDisruption
from llm_support.schemas import ExplanationResponse
from network_monitoring.schemas import NetworkHealthReport
from simulation_engine.schemas import SimulationInput, SimulationResult


@dataclass
class SystemRunnerConfig:
    mode: str  # "baseline", "disruption", "allocation", "simulation", "monitoring"


@dataclass
class SystemRunnerInput:
    decision_input: DecisionCoordinatorInput
    disruption_scenario: Optional[DisruptionScenario] = None
    simulation_input: Optional[SimulationInput] = None
    allocation_request: Optional[AllocationRequest] = None
    explanation_task: Optional[str] = None
    explanation_question: Optional[str] = None


@dataclass
class SystemRunnerResult:
    core_result: Optional[DecisionCoordinatorResult] = None
    disruption_result: Optional[ResolvedDisruption] = None
    allocation_result: Optional[AllocationResult] = None
    simulation_result: Optional[SimulationResult] = None
    monitoring_result: Optional[NetworkHealthReport] = None
    llm_explanation: Optional[ExplanationResponse] = None