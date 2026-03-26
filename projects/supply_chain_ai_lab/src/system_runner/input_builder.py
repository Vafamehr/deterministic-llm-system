from decision_coordinator.schemas import DecisionCoordinatorInput
from tools.schemas import (
    ForecastToolInput,
    InventoryStatusToolInput,
    ReplenishmentToolInput,
)
from replenishment.schemas import ReplenishmentInput

from sample_data.sample_network import build_sample_network
from sample_data.synthetic_demand_history import generate_synthetic_demand_history

from demand_forecasting.schemas import DemandRecord, DemandDataset
from demand_forecasting.features import build_feature_rows_for_dataset
from demand_forecasting.model import run_linear_regression_training
from allocation.schemas import AllocationRequest, LocationDemand

from simulation_engine.schemas import SimulationInput
from simulation_engine.scenarios import (
    build_baseline_scenario,
    build_demand_spike_scenario,
    build_supplier_delay_scenario,
)

from disruption_modeling.schemas import DisruptionScenario
from system_runner.schemas import SystemRunnerInput


# =========================
# CORE BUILDERS
# =========================

def build_decision_input(
    sku_id: str | None = None,
    location_id: str | None = None,
) -> DecisionCoordinatorInput:
    network = build_sample_network()
    demand_df = generate_synthetic_demand_history()

    inventory_record = None
    series_df = None

    if sku_id is not None and location_id is not None:
        for record in network.inventory:
            if record.sku_id == sku_id and record.location_id == location_id:
                candidate_df = demand_df[
                    (demand_df["sku_id"] == record.sku_id)
                    & (demand_df["location_id"] == record.location_id)
                ].sort_values("date")

                if not candidate_df.empty:
                    inventory_record = record
                    series_df = candidate_df
                    break

        if inventory_record is None or series_df is None:
            raise ValueError(
                f"No valid data found for sku_id={sku_id}, location_id={location_id}"
            )
    else:
        for record in network.inventory:
            candidate_df = demand_df[
                (demand_df["sku_id"] == record.sku_id)
                & (demand_df["location_id"] == record.location_id)
            ].sort_values("date")

            if not candidate_df.empty:
                inventory_record = record
                series_df = candidate_df
                break

        if inventory_record is None or series_df is None:
            raise ValueError("No inventory record matched any demand series.")

    # --- TEMP TEST OVERRIDE (OVERSTOCK CASE) ---
    # Remove after validation.
    # inventory_record.on_hand = 800
    # inventory_record.on_order = 0
    # inventory_record.reserved = 0

    selected_sku_id = inventory_record.sku_id
    selected_location_id = inventory_record.location_id

    series_records = [
        DemandRecord(
            sku_id=row["sku_id"],
            location_id=row["location_id"],
            date=row["date"],
            demand=float(row["units_sold"]),
        )
        for row in series_df.to_dict(orient="records")
    ]

    dataset_records = [
        DemandRecord(
            sku_id=row["sku_id"],
            location_id=row["location_id"],
            date=row["date"],
            demand=float(row["units_sold"]),
        )
        for row in demand_df.to_dict(orient="records")
    ]
    dataset = DemandDataset(records=dataset_records)

    feature_rows = build_feature_rows_for_dataset(dataset)
    model, _ = run_linear_regression_training(feature_rows)

    forecast_input = ForecastToolInput(
        model=model,
        series_records=series_records,
        horizon=3,
    )

    inventory_input = InventoryStatusToolInput(
        record=inventory_record,
        expected_daily_demand=0.0,
        lead_time_days=3,
    )

    replenishment_input = ReplenishmentInput(
        sku_id=selected_sku_id,
        location_id=selected_location_id,
        inventory_position=(
            inventory_record.on_hand
            + inventory_record.on_order
            - inventory_record.reserved
        ),
        expected_daily_demand=0.0,
        lead_time_days=3,
        safety_stock=20,
    )

    replenishment_tool_input = ReplenishmentToolInput(
        replenishment_input=replenishment_input
    )

    return DecisionCoordinatorInput(
        forecast_input=forecast_input,
        inventory_input=inventory_input,
        replenishment_input=replenishment_tool_input,
    )


def build_allocation_request_from_network() -> AllocationRequest:
    network = build_sample_network()
    demand_df = generate_synthetic_demand_history()

    sku_id = network.inventory[0].sku_id

    supply_record = None
    for record in network.inventory:
        if "wh" in record.location_id.lower() or "dc" in record.location_id.lower():
            supply_record = record
            break

    if supply_record is None:
        supply_record = network.inventory[0]

    available_inventory = (
        supply_record.on_hand
        + supply_record.on_order
        - supply_record.reserved
    )

    location_demands = []

    store_records = [
        r for r in network.inventory
        if r.location_id != supply_record.location_id
    ]

    for record in store_records:
        store_df = demand_df[
            (demand_df["sku_id"] == record.sku_id)
            & (demand_df["location_id"] == record.location_id)
        ]

        if store_df.empty:
            continue

        demand_units = float(store_df["units_sold"].mean())

        location_demands.append(
            LocationDemand(
                location_id=record.location_id,
                demand_units=demand_units,
            )
        )

    if not location_demands:
        raise ValueError("No store demand found for allocation.")

    return AllocationRequest(
        sku_id=sku_id,
        available_inventory=available_inventory,
        location_demands=location_demands,
    )


def build_simulation_input(
    sku_id: str | None = None,
    location_id: str | None = None,
) -> SimulationInput:
    baseline_input = build_decision_input(
        sku_id=sku_id,
        location_id=location_id,
    )

    scenarios = [
        build_baseline_scenario(),
        build_demand_spike_scenario(),
        build_supplier_delay_scenario(),
    ]

    return SimulationInput(
        baseline_input=baseline_input,
        scenarios=scenarios,
    )


# =========================
# RUNNER BUILDERS
# =========================

def build_baseline_runner_input(
    sku_id: str | None = None,
    location_id: str | None = None,
) -> SystemRunnerInput:
    return SystemRunnerInput(
        decision_input=build_decision_input(
            sku_id=sku_id,
            location_id=location_id,
        ),
        simulation_input=None,
        disruption_scenario=None,
        allocation_request=None,
        explanation_task=None,
        explanation_question=None,
    )


def build_simulation_runner_input(
    explanation_task: str = "scenario_comparison",
    explanation_question: str | None = None,
    sku_id: str | None = None,
    location_id: str | None = None,
) -> SystemRunnerInput:
    return SystemRunnerInput(
        decision_input=build_decision_input(
            sku_id=sku_id,
            location_id=location_id,
        ),
        simulation_input=build_simulation_input(
            sku_id=sku_id,
            location_id=location_id,
        ),
        disruption_scenario=None,
        allocation_request=None,
        explanation_task=explanation_task,
        explanation_question=explanation_question,
    )


def build_disruption_runner_input(
    disruption_scenario: DisruptionScenario,
    sku_id: str | None = None,
    location_id: str | None = None,
) -> SystemRunnerInput:
    return SystemRunnerInput(
        decision_input=build_decision_input(
            sku_id=sku_id,
            location_id=location_id,
        ),
        simulation_input=None,
        disruption_scenario=disruption_scenario,
        allocation_request=None,
        explanation_task=None,
        explanation_question=None,
    )


def build_allocation_runner_input() -> SystemRunnerInput:
    return SystemRunnerInput(
        decision_input=build_decision_input(),
        simulation_input=None,
        disruption_scenario=None,
        allocation_request=build_allocation_request_from_network(),
        explanation_task=None,
        explanation_question=None,
    )