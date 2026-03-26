from disruption_modeling.schemas import (
    AffectedNode,
    DisruptionEvent,
    DisruptionImpact,
    DisruptionScenario,
    DisruptionType,
    SeverityLevel,
)
from llm_support.schemas import ExplanationTask
from system_runner.input_builder import (
    build_allocation_runner_input,
    build_baseline_runner_input,
    build_disruption_runner_input,
    build_simulation_runner_input,
)
from system_runner.schemas import SystemRunnerConfig
from system_runner.service import run_supply_chain_system


def build_sample_disruption_scenario() -> DisruptionScenario:
    event = DisruptionEvent(
        event_id="event_1",
        disruption_type=DisruptionType.SUPPLIER_DELAY,
        severity=SeverityLevel.HIGH,
        duration_days=3,
        affected_node=AffectedNode(
            node_id="supplier_1",
            node_type="supplier",
        ),
        description="Supplier delay due to capacity issues",
    )

    impact = DisruptionImpact(
        demand_multiplier=1.5,
        inventory_loss_units=30,
        supplier_delay_days=2,
    )

    return DisruptionScenario(
        scenario_name="supplier_delay_scenario",
        event=event,
        impact=impact,
    )


def print_selected_context(system_input) -> None:
    record = system_input.decision_input.inventory_input.record

    print("\n=== SELECTED CONTEXT ===")
    print(f"SKU: {record.sku_id}")
    print(f"Location: {record.location_id}")
    print(f"On Hand: {record.on_hand}")
    print(f"On Order: {record.on_order}")
    print(f"Reserved: {record.reserved}")


def print_core_result(core_result) -> None:
    print("\n=== CORE DECISION RESULT ===")
    print(f"Forecast: {core_result.forecast_result.forecast_values}")
    print(
        f"Expected Daily Demand: "
        f"{core_result.inventory_result.expected_daily_demand:.2f}"
    )
    print(f"Days of Supply: {core_result.inventory_result.days_of_supply:.2f}")
    print(f"Stockout Risk: {core_result.inventory_result.stockout_risk}")
    print(f"Reorder: {core_result.replenishment_result.reorder}")
    print(
        f"Recommended Units: "
        f"{core_result.replenishment_result.recommended_units:.2f}"
    )


def print_disruption_result(disruption_result) -> None:
    print("\n=== DISRUPTION RESULT ===")
    print(f"Scenario: {disruption_result.scenario_name}")
    print(f"Demand Multiplier: {disruption_result.impact.demand_multiplier}")
    print(f"Inventory Loss Units: {disruption_result.impact.inventory_loss_units}")
    print(f"Supplier Delay Days: {disruption_result.impact.supplier_delay_days}")
    print(
        f"Warehouse Capacity Multiplier: "
        f"{disruption_result.impact.warehouse_capacity_multiplier}"
    )
    print(
        f"Transportation Delay Days: "
        f"{disruption_result.impact.transportation_delay_days}"
    )


def print_allocation_result(allocation_result) -> None:
    print("\n=== ALLOCATION RESULT ===")
    print(f"SKU: {allocation_result.sku_id}")

    for allocation in allocation_result.allocations:
        print(
            f"{allocation.location_id:<15} "
            f"allocated_units={allocation.allocated_units:.2f}"
        )


def print_simulation_result(simulation_result) -> None:
    print("\n=== SCENARIO ANALYSIS + V4 ===")

    if simulation_result.analysis_result is None:
        print("No scenario analysis result produced.")
        return

    for row in simulation_result.analysis_result.comparison_rows:
        state = (
            row.decision_intelligence.inventory_state
            if row.decision_intelligence
            else None
        )
        key_risk = (
            row.decision_intelligence.key_risk
            if row.decision_intelligence
            else None
        )

        print(
            f"{row.scenario_name:<15} "
            f"reorder={str(row.reorder):<6} "
            f"units={row.recommended_units:<10.2f} "
            f"delta={row.delta_vs_baseline:<10.2f} "
            f"dos={row.days_of_supply:<8.2f} "
            f"risk={str(row.stockout_risk):<6} "
            f"pressure={row.inventory_pressure:<6} "
            f"overstock={row.overstock_risk:<6} "
            f"state={state} "
            f"key_risk={key_risk}"
        )


def print_llm_explanation(llm_explanation) -> None:
    print("\n=== LLM EXPLANATION ===")
    print(f"Task: {llm_explanation.task}")
    print(llm_explanation.explanation_text)


def main() -> None:
    mode = "simulation"  # CHANGE THIS IF NEEDED

    # Optional explicit selection.
    # Leave as None/None to use fallback behavior from input_builder.
    sku_id = None
    location_id = None

    config = SystemRunnerConfig(mode=mode)

    if mode == "baseline":
        system_input = build_baseline_runner_input(
            sku_id=sku_id,
            location_id=location_id,
        )
    elif mode == "simulation":
        system_input = build_simulation_runner_input(
            explanation_task=ExplanationTask.SCENARIO_COMPARISON,
            explanation_question=None,
            sku_id=sku_id,
            location_id=location_id,
        )
    elif mode == "disruption":
        system_input = build_disruption_runner_input(
            disruption_scenario=build_sample_disruption_scenario(),
            sku_id=sku_id,
            location_id=location_id,
        )
    elif mode == "allocation":
        system_input = build_allocation_runner_input()
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    print_selected_context(system_input)

    result = run_supply_chain_system(config, system_input)

    if result.core_result is not None:
        print_core_result(result.core_result)

    if result.disruption_result is not None:
        print_disruption_result(result.disruption_result)

    if result.allocation_result is not None:
        print_allocation_result(result.allocation_result)

    if result.simulation_result is not None:
        print_simulation_result(result.simulation_result)

    if result.llm_explanation is not None:
        print_llm_explanation(result.llm_explanation)

    if (
        result.core_result is None
        and result.disruption_result is None
        and result.allocation_result is None
        and result.simulation_result is None
        and result.monitoring_result is None
        and result.llm_explanation is None
    ):
        print("No result produced.")


if __name__ == "__main__":
    main()