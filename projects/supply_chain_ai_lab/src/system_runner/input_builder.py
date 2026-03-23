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


def build_decision_input() -> DecisionCoordinatorInput:
    """
    Build DecisionCoordinatorInput using a real trained forecasting model.
    """

    # --- STEP 1: Load network ---
    network = build_sample_network()

    # --- STEP 2: Demand history ---
    demand_df = generate_synthetic_demand_history()

    # Pick an inventory record that actually has matching demand history
    inventory_record = None
    series_df = None

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

    sku_id = inventory_record.sku_id
    location_id = inventory_record.location_id

    # --- STEP 3: Build one series for inference ---
    series_records = [
        DemandRecord(
            sku_id=row["sku_id"],
            location_id=row["location_id"],
            date=row["date"],
            demand=float(row["units_sold"]),
        )
        for row in series_df.to_dict(orient="records")
    ]

    # --- STEP 4: Build full dataset for training ---
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

    # --- STEP 5: Train model ---
    feature_rows = build_feature_rows_for_dataset(dataset)
    model, _ = run_linear_regression_training(feature_rows)

    # --- STEP 6: Forecast input ---
    forecast_input = ForecastToolInput(
        model=model,
        series_records=series_records,
        horizon=3,
    )

    # --- STEP 7: Inventory input ---
    inventory_input = InventoryStatusToolInput(
        record=inventory_record,
        expected_daily_demand=0.0,
        lead_time_days=3,
    )

    # --- STEP 8: Replenishment input ---
    replenishment_input = ReplenishmentInput(
        sku_id=sku_id,
        location_id=location_id,
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
    """
    Build AllocationRequest using real network + demand data.

    - available_inventory → from a warehouse/DC
    - location_demands → aggregated recent demand per store
    """

    # --- STEP 1: Load network + demand ---
    network = build_sample_network()
    demand_df = generate_synthetic_demand_history()

    # --- STEP 2: Choose SKU ---
    sku_id = network.inventory[0].sku_id

    # --- STEP 3: Pick a supply location (warehouse/DC) ---
    # simple rule: pick first non-store location
    supply_record = None
    for record in network.inventory:
        if "wh" in record.location_id.lower() or "dc" in record.location_id.lower():
            supply_record = record
            break

    if supply_record is None:
        # fallback: just pick first record
        supply_record = network.inventory[0]

    available_inventory = (
        supply_record.on_hand
        + supply_record.on_order
        - supply_record.reserved
    )

    # --- STEP 4: Build store demand ---
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

        # simple aggregation: average recent demand
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


def build_simulation_input() -> SimulationInput:
    """
    Build SimulationInput using existing decision input + predefined scenarios.
    """

    baseline_input = build_decision_input()

    scenarios = [
        build_baseline_scenario(),
        build_demand_spike_scenario(),
        build_supplier_delay_scenario(),
    ]

    return SimulationInput(
        baseline_input=baseline_input,
        scenarios=scenarios,
    )