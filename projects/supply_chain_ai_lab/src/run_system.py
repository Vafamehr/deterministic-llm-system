from allocation.schemas import AllocationRequest, LocationDemand
from disruption_modeling.schemas import (
    AffectedNode,
    DisruptionEvent,
    DisruptionImpact,
    DisruptionScenario,
    DisruptionType,
    SeverityLevel,
)
from system_runner.input_builder import (
    build_allocation_request_from_network,
    build_decision_input,
    build_simulation_input,
)
from system_runner.schemas import SystemRunnerConfig, SystemRunnerInput
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


def print_simulation_result(simulation_result) -> None:
    print("\n=== SIMULATION ===")

    # --- BASELINE ---
    if simulation_result.baseline_result is not None:
        print("\nBaseline:")
        print(
            "Reorder: "
            f"{simulation_result.baseline_result.replenishment_result.should_reorder}"
        )
        print(
            "Recommended Units: "
            f"{round(simulation_result.baseline_result.replenishment_result.recommended_order_units, 2)}"
        )

    # --- SCENARIOS ---
    for scenario_result in simulation_result.scenario_results:
        print(f"\nScenario: {scenario_result.scenario.name}")
        print(
            "Reorder: "
            f"{scenario_result.decision_result.replenishment_result.should_reorder}"
        )
        print(
            "Recommended Units: "
            f"{round(scenario_result.decision_result.replenishment_result.recommended_order_units, 2)}"
        )

    # --- ANALYSIS (FINAL CLEAN OUTPUT) ---
    if simulation_result.analysis_result is not None:
        print("\n=== SCENARIO ANALYSIS ===")
        for row in simulation_result.analysis_result.comparison_rows:
            print(
                f"{row.scenario_name:<15} "
                f"reorder={str(row.reorder):<6} "
                f"units={row.recommended_units:<10.2f} "
                f"delta={row.delta_vs_baseline:<10.2f} "
                f"dos={row.days_of_supply:<8.2f} "
                f"risk={row.stockout_risk:<6} "
                f"pressure={row.inventory_pressure:<6}"
            )


def main():
    mode = "simulation"  # CHANGE THIS IF NEEDED

    config = SystemRunnerConfig(mode=mode)
    decision_input = build_decision_input()

    disruption_scenario = None
    allocation_request = None
    simulation_input = None

    if mode == "disruption":
        disruption_scenario = build_sample_disruption_scenario()

    if mode == "allocation":
        allocation_request = build_allocation_request_from_network()

    if mode == "simulation":
        simulation_input = build_simulation_input()

    system_input = SystemRunnerInput(
        decision_input=decision_input,
        disruption_scenario=disruption_scenario,
        simulation_input=simulation_input,
        allocation_request=allocation_request,
    )

    result = run_supply_chain_system(config, system_input)

    # --- SIMULATION OUTPUT ---
    if result.simulation_result is not None:
        print_simulation_result(result.simulation_result)
        return

    print("No simulation result produced.")


if __name__ == "__main__":
    main()