from dataclasses import replace
from typing import List

from decision_coordinator.schemas import DecisionCoordinatorInput
from decision_coordinator.service import run_supply_chain_decision
from scenario_analysis.service import ScenarioAnalysisService
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
    forecast_input = baseline_input.forecast_input
    inventory_input = baseline_input.inventory_input
    replenishment_tool_input = baseline_input.replenishment_input
    replenishment_input = replenishment_tool_input.replenishment_input

    demand_multiplier_override = baseline_input.demand_multiplier_override

    if scenario.demand_multiplier != 1.0:
        if demand_multiplier_override is None:
            demand_multiplier_override = scenario.demand_multiplier
        else:
            demand_multiplier_override *= scenario.demand_multiplier

    if scenario.lead_time_multiplier != 1.0:
        updated_inventory_lead_time = max(
            1,
            int(inventory_input.lead_time_days * scenario.lead_time_multiplier),
        )
        updated_replenishment_lead_time = max(
            1,
            int(replenishment_input.lead_time_days * scenario.lead_time_multiplier),
        )

        inventory_input = replace(
            inventory_input,
            lead_time_days=updated_inventory_lead_time,
        )

        replenishment_input = replace(
            replenishment_input,
            lead_time_days=updated_replenishment_lead_time,
        )

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
        demand_multiplier_override=demand_multiplier_override,
    )

    return simulated_input


def run_simulation(simulation_input: SimulationInput) -> SimulationResult:
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

    simulation_result = SimulationResult(
        baseline_input=simulation_input.baseline_input,
        baseline_result=baseline_result,
        scenario_results=scenario_results,
    )

    analysis_service = ScenarioAnalysisService()
    analysis_result = analysis_service.analyze(simulation_result)

    simulation_result = replace(
        simulation_result,
        analysis_result=analysis_result,
    )

    return simulation_result