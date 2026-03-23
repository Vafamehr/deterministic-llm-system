from dataclasses import replace

from decision_coordinator.service import run_supply_chain_decision
from disruption_modeling.service import resolve_disruption

from system_runner.schemas import (
    SystemRunnerConfig,
    SystemRunnerInput,
    SystemRunnerResult,
)


def _apply_disruption(decision_input, impact):
    """
    Apply disruption impact directly to existing tool inputs.

    Notes:
    - frozen tool input wrappers are updated via dataclasses.replace
    - inner domain objects can still be mutated if they are not frozen
    """

    forecast_input = decision_input.forecast_input
    inventory_input = decision_input.inventory_input
    replenishment_tool_input = decision_input.replenishment_input

    # ---------------------------------


    # ---------------------------------
    # 2) INVENTORY LOSS -> inventory + replenishment position
    # ---------------------------------
    if impact.inventory_loss_units > 0:
        inventory_record = inventory_input.record
        inventory_record.on_hand = max(
            0,
            inventory_record.on_hand - impact.inventory_loss_units,
        )

        replenishment_input = replenishment_tool_input.replenishment_input
        replenishment_input.inventory_position = max(
            0,
            replenishment_input.inventory_position - impact.inventory_loss_units,
        )

    # ---------------------------------
    # 3) DELAYS -> lead times
    # ---------------------------------
    delay_days = (
        impact.supplier_delay_days
        + impact.transportation_delay_days
    )

    if delay_days > 0:
        inventory_input = replace(
            inventory_input,
            lead_time_days=inventory_input.lead_time_days + delay_days,
        )

        updated_replenishment_input = replace(
            replenishment_tool_input.replenishment_input,
            lead_time_days=(
                replenishment_tool_input.replenishment_input.lead_time_days
                + delay_days
            ),
        )

        replenishment_tool_input = replace(
            replenishment_tool_input,
            replenishment_input=updated_replenishment_input,
        )

    decision_input = replace(
        decision_input,
        forecast_input=forecast_input,
        inventory_input=inventory_input,
        replenishment_input=replenishment_tool_input,
    )

    return decision_input


def run_supply_chain_system(
    config: SystemRunnerConfig,
    system_input: SystemRunnerInput,
) -> SystemRunnerResult:
    """
    Top-level orchestration layer.
    """

    disruption_result = None
    decision_input = system_input.decision_input

    # --- STEP 1: Resolve/apply disruption before core decision ---
    if config.mode == "disruption":
        if system_input.disruption_scenario is None:
            raise ValueError(
                "disruption_scenario is required when mode='disruption'."
            )

        disruption_result = resolve_disruption(system_input.disruption_scenario)
        decision_input = replace(
        decision_input,
        disruption_impact=disruption_result.impact
        )
        decision_input = _apply_disruption(
            decision_input,
            disruption_result.impact,
        )

    # --- STEP 2: Run core decision engine ---
    core_result = run_supply_chain_decision(decision_input)

    # --- STEP 3: Return unified result ---
    return SystemRunnerResult(
        core_result=core_result,
        disruption_result=disruption_result,
        allocation_result=None,
        simulation_result=None,
        monitoring_result=None,
    )