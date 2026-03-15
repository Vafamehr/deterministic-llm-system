from dataclasses import replace
from typing import List

from decision_coordinator.schemas import DecisionCoordinatorInput
from decision_coordinator.service import run_supply_chain_decision
from simulation_engine.schemas import (
    Scenario,
    ScenarioResult,
    SimulationInput,
    SimulationResult,
)


def _apply_scenario_modifications(
    baseline_input: DecisionCoordinatorInput,
    scenario: Scenario,
) -> DecisionCoordinatorInput:
    """
    Apply deterministic scenario adjustments by creating updated copies
    of frozen tool-input dataclasses.

    The simulation layer modifies the actual tool inputs that drive the
    downstream decision flow.
    """

    forecast_input = baseline_input.forecast_input
    inventory_input = baseline_input.inventory_input
    replenishment_tool_input = baseline_input.replenishment_input
    replenishment_input = replenishment_tool_input.replenishment_input

    # -------------------------------------------------------------
    # Demand shock
    # -------------------------------------------------------------
    if scenario.demand_multiplier != 1.0:
        inventory_input = replace(
            inventory_input,
            expected_daily_demand=(
                inventory_input.expected_daily_demand * scenario.demand_multiplier
            ),
        )

        replenishment_input = replace(
            replenishment_input,
            expected_daily_demand=(
                replenishment_input.expected_daily_demand * scenario.demand_multiplier
            ),
        )

    # -------------------------------------------------------------
    # Lead time shock
    # -------------------------------------------------------------
    if scenario.lead_time_multiplier != 1.0:
        inventory_input = replace(
            inventory_input,
            lead_time_days=int(
                inventory_input.lead_time_days * scenario.lead_time_multiplier
            ),
        )

        replenishment_input = replace(
            replenishment_input,
            lead_time_days=int(
                replenishment_input.lead_time_days * scenario.lead_time_multiplier
            ),
        )

    # -------------------------------------------------------------
    # Inventory shock
    # -------------------------------------------------------------
    if scenario.inventory_multiplier != 1.0:
        updated_record = replace(
            inventory_input.record,
            on_hand=inventory_input.record.on_hand * scenario.inventory_multiplier,
        )

        inventory_input = replace(
            inventory_input,
            record=updated_record,
        )

        replenishment_input = replace(
            replenishment_input,
            inventory_position=(
                replenishment_input.inventory_position * scenario.inventory_multiplier
            ),
        )

    updated_replenishment_tool_input = replace(
        replenishment_tool_input,
        replenishment_input=replenishment_input,
    )

    simulated_input = replace(
        baseline_input,
        forecast_input=forecast_input,
        inventory_input=inventory_input,
        replenishment_input=updated_replenishment_tool_input,
    )

    return simulated_input


def run_simulation(simulation_input: SimulationInput) -> SimulationResult:
    """
    Execute a baseline run plus all scenario runs.
    """

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