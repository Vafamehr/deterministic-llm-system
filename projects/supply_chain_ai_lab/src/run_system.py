from system_runner.service import run_supply_chain_system
from system_runner.schemas import SystemRunnerConfig, SystemRunnerInput
from system_runner.input_builder import build_decision_input

from disruption_modeling.schemas import (
    DisruptionScenario,
    DisruptionEvent,
    DisruptionImpact,
    DisruptionType,
    SeverityLevel,
    AffectedNode,
)


def build_sample_disruption_scenario() -> DisruptionScenario:
    """
    Create a simple disruption scenario for testing.
    """
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


def print_forecast_result(forecast_result) -> None:
    print("\n=== FORECAST ===")
    print(f"SKU: {forecast_result.sku_id}")
    print(f"Location: {forecast_result.location_id}")
    print(f"Horizon: {forecast_result.horizon}")
    rounded_predictions = [round(value, 2) for value in forecast_result.predicted_values]
    print(f"Predictions: {rounded_predictions}")


def print_inventory_result(inventory_result) -> None:
    print("\n=== INVENTORY ===")
    print(f"SKU: {inventory_result.sku_id}")
    print(f"Location: {inventory_result.location_id}")
    print(f"Inventory Position: {round(inventory_result.inventory_position, 2)}")
    print(f"Days of Supply: {round(inventory_result.days_of_supply, 2)}")
    print(f"Stockout Risk: {inventory_result.stockout_risk}")


def print_replenishment_result(replenishment_result) -> None:
    print("\n=== REPLENISHMENT ===")
    print(f"SKU: {replenishment_result.sku_id}")
    print(f"Location: {replenishment_result.location_id}")
    print(f"Reorder Point: {round(replenishment_result.reorder_point, 2)}")
    print(f"Should Reorder: {replenishment_result.should_reorder}")
    print(f"Recommended Units: {round(replenishment_result.recommended_order_units, 2)}")

    if replenishment_result.reason_codes:
        print("Reasons:")
        for reason in replenishment_result.reason_codes:
            print(f"  - {reason}")
    else:
        print("Reasons: None")


def main():
    mode = "disruption"  # change to "baseline" to compare

    config = SystemRunnerConfig(mode=mode)
    decision_input = build_decision_input()

    disruption_scenario = None
    if mode == "disruption":
        disruption_scenario = build_sample_disruption_scenario()

    system_input = SystemRunnerInput(
        decision_input=decision_input,
        disruption_scenario=disruption_scenario,
    )

    result = run_supply_chain_system(config, system_input)

    print_forecast_result(result.core_result.forecast_result)
    print_inventory_result(result.core_result.inventory_result)
    print_replenishment_result(result.core_result.replenishment_result)


if __name__ == "__main__":
    main()