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