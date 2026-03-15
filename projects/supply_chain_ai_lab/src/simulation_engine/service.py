from copy import deepcopy
from typing import List

from simulation_engine.schemas import (
    SimulationInput,
    SimulationResult,
    ScenarioResult,
    Scenario,
)

from decision_coordinator.service import run_supply_chain_decision
from decision_coordinator.schemas import (
    DecisionCoordinatorInput,
)


def _apply_scenario_modifications(
    baseline_input: DecisionCoordinatorInput,
    scenario: Scenario,
) -> DecisionCoordinatorInput:
    """
    Applies scenario adjustments to a copy of the baseline input.

    For V1 we keep the modifications simple and deterministic.
    """

    simulated_input = deepcopy(baseline_input)

    # --- Modify forecast demand assumptions if needed ---
    if scenario.demand_multiplier != 1.0:
        try:
            simulated_input.forecast_input.demand_multiplier *= scenario.demand_multiplier
        except AttributeError:
            pass

    # --- Modify lead time assumptions ---
    if scenario.lead_time_multiplier != 1.0:
        try:
            simulated_input.replenishment_input.lead_time_days = int(
                simulated_input.replenishment_input.lead_time_days
                * scenario.lead_time_multiplier
            )
        except AttributeError:
            pass

    # --- Modify inventory assumptions ---
    if scenario.inventory_multiplier != 1.0:
        try:
            simulated_input.inventory_input.inventory_multiplier *= scenario.inventory_multiplier
        except AttributeError:
            pass

    return simulated_input


def run_simulation(simulation_input: SimulationInput) -> SimulationResult:
    """
    Executes a full simulation run.

    Steps:
    1. Run baseline decision pipeline
    2. Run each scenario variation
    3. Collect results
    """

    # --- Baseline run ---
    baseline_result = run_supply_chain_decision(
        simulation_input.baseline_input
    )

    scenario_results: List[ScenarioResult] = []

    for scenario in simulation_input.scenarios:

        simulated_input = _apply_scenario_modifications(
            simulation_input.baseline_input,
            scenario,
        )

        decision_result = run_supply_chain_decision(simulated_input)

        scenario_results.append(
            ScenarioResult(
                scenario=scenario,
                simulated_input=simulated_input,
                decision_result=decision_result,
            )
        )

    return SimulationResult(
        baseline_input=simulation_input.baseline_input,
        baseline_result=baseline_result,
        scenario_results=scenario_results,
    )