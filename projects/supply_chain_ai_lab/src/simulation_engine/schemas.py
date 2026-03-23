from dataclasses import dataclass, field
from typing import List, Optional, Dict

from decision_coordinator.schemas import (
    DecisionCoordinatorInput,
    DecisionCoordinatorResult,
)
from scenario_analysis.schemas import ScenarioAnalysisResult


@dataclass
class Scenario:
    """
    Defines a simulation scenario.

    The scenario describes how the baseline system state
    should be modified before running the decision pipeline.
    """

    name: str
    description: str

    demand_multiplier: float = 1.0
    lead_time_multiplier: float = 1.0
    inventory_multiplier: float = 1.0

    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class SimulationInput:
    """
    Input to the simulation engine.

    baseline_input:
        The normal coordinator input representing the real system state.

    scenarios:
        A list of scenarios to run against the same baseline.
    """

    baseline_input: DecisionCoordinatorInput
    scenarios: List[Scenario]


@dataclass
class ScenarioResult:
    """
    Result produced by executing one scenario.
    """

    scenario: Scenario

    simulated_input: DecisionCoordinatorInput

    decision_result: DecisionCoordinatorResult

    notes: Optional[str] = None


@dataclass
class SimulationResult:
    """
    Aggregate output of a simulation run.
    """

    baseline_input: DecisionCoordinatorInput

    baseline_result: Optional[DecisionCoordinatorResult]

    scenario_results: List[ScenarioResult]
    analysis_result: Optional[ScenarioAnalysisResult] = None