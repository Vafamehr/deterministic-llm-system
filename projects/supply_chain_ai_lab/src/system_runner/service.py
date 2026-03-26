from dataclasses import replace

from allocation.service import allocate_inventory
from decision_coordinator.service import run_supply_chain_decision
from disruption_modeling.service import resolve_disruption
from llm_support.service import LLMExplanationService
from network_monitoring.schemas import NetworkInventoryRecord
from network_monitoring.service import build_network_health_report
from simulation_engine.service import run_simulation

from system_runner.schemas import (
    SystemRunnerConfig,
    SystemRunnerInput,
    SystemRunnerResult,
)


def _apply_disruption(decision_input, impact):
    forecast_input = decision_input.forecast_input
    inventory_input = decision_input.inventory_input
    replenishment_tool_input = decision_input.replenishment_input

    # 1) DEMAND SHOCK -> inventory + replenishment demand inputs
    if impact.demand_multiplier != 1.0:
        inventory_input = replace(
            inventory_input,
            expected_daily_demand=(
                inventory_input.expected_daily_demand * impact.demand_multiplier
            ),
        )

        updated_replenishment_input = replace(
            replenishment_tool_input.replenishment_input,
            expected_daily_demand=(
                replenishment_tool_input.replenishment_input.expected_daily_demand
                * impact.demand_multiplier
            ),
        )

        replenishment_tool_input = replace(
            replenishment_tool_input,
            replenishment_input=updated_replenishment_input,
        )

    # 2) INVENTORY LOSS -> inventory + replenishment position
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

    # 3) DELAYS -> lead times
    delay_days = impact.supplier_delay_days + impact.transportation_delay_days

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
    disruption_result = None
    decision_input = system_input.decision_input

    if config.mode == "allocation":
        if system_input.allocation_request is None:
            raise ValueError(
                "allocation_request is required when mode='allocation'."
            )

        allocation_result = allocate_inventory(
            system_input.allocation_request
        )

        return SystemRunnerResult(
            core_result=None,
            disruption_result=None,
            allocation_result=allocation_result,
            simulation_result=None,
            monitoring_result=None,
            llm_explanation=None,
        )

    if config.mode == "simulation":
        if system_input.simulation_input is None:
            raise ValueError(
                "simulation_input is required when mode='simulation'."
            )

        simulation_result = run_simulation(system_input.simulation_input)

        # --- V4 PRINT (LIGHT, NO REFACTOR) ---
        if simulation_result.analysis_result is not None:
            print("\n=== SCENARIO ANALYSIS + V4 ===")

            for row in simulation_result.analysis_result.comparison_rows:
                state = (
                    row.decision_intelligence.inventory_state
                    if row.decision_intelligence
                    else None
                )
                risk = (
                    row.decision_intelligence.key_risk
                    if row.decision_intelligence
                    else None
                )

                print(
                    f"{row.scenario_name:<15}"
                    f" reorder={row.reorder:<5}"
                    f" units={row.recommended_units:<10.2f}"
                    f" delta={row.delta_vs_baseline:<10.2f}"
                    f" dos={row.days_of_supply:<8.2f}"
                    f" risk={row.stockout_risk:<6}"
                    f" pressure={row.inventory_pressure:<6}"
                    f" overstock={row.overstock_risk:<6}"
                    f" state={state}"
                    f" key_risk={risk}"
                )

        llm_explanation = None
        if system_input.explanation_task is not None:
            llm_service = LLMExplanationService()
            llm_explanation = llm_service.explain(
                simulation_result=simulation_result,
                task=system_input.explanation_task,
            )

        return SystemRunnerResult(
            core_result=None,
            disruption_result=None,
            allocation_result=None,
            simulation_result=simulation_result,
            monitoring_result=None,
            llm_explanation=llm_explanation,
        )

    if config.mode == "disruption":
        if system_input.disruption_scenario is None:
            raise ValueError(
                "disruption_scenario is required when mode='disruption'."
            )

        disruption_result = resolve_disruption(system_input.disruption_scenario)
        decision_input = replace(
            decision_input,
            disruption_impact=disruption_result.impact,
        )
        decision_input = _apply_disruption(
            decision_input,
            disruption_result.impact,
        )

    core_result = run_supply_chain_decision(decision_input)

    monitoring_result = None
    if config.mode == "monitoring":
        inventory_result = core_result.inventory_result
        inventory_record = NetworkInventoryRecord(
            sku_id=inventory_result.sku_id,
            location_id=inventory_result.location_id,
            on_hand=inventory_result.inventory_position,
            expected_daily_demand=decision_input.inventory_input.expected_daily_demand,
        )

        monitoring_result = build_network_health_report(
            inventory_records=[inventory_record]
        )

    return SystemRunnerResult(
        core_result=core_result,
        disruption_result=disruption_result,
        allocation_result=None,
        simulation_result=None,
        monitoring_result=monitoring_result,
        llm_explanation=None,
    )