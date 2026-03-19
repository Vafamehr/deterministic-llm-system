from pathlib import Path

from demand_forecasting.data import load_demand_dataset
from demand_forecasting.data_loader import load_demand_history
from demand_forecasting.features import build_feature_rows_for_dataset
from demand_forecasting.model import run_linear_regression_training
from demand_forecasting.schemas import DemandRecord
from demand_forecasting.tool_input_builder import build_forecast_tool_input

from sample_data.sample_network import build_sample_network

from decision_coordinator.service import run_supply_chain_decision
from decision_coordinator.schemas import DecisionCoordinatorInput

from tools.schemas import (
    InventoryStatusToolInput,
    ReplenishmentToolInput,
)

from replenishment.schemas import ReplenishmentInput


def main() -> None:
    # -------------------------------
    # 1. Load demand history CSV
    # -------------------------------
    src_root = Path(__file__).resolve().parents[1]
    csv_path = src_root / "sample_data" / "synthetic_demand_history.csv"

    demand_df = load_demand_history(csv_path)

    # -------------------------------
    # 2. Convert DataFrame -> DemandDataset
    #    for model training path
    # -------------------------------
    records = [
        DemandRecord(
            sku_id=row["sku_id"],
            location_id=row["location_id"],
            date=row["date"].date() if hasattr(row["date"], "date") else row["date"],
            demand=float(row["units_sold"]),
        )
        for _, row in demand_df.iterrows()
    ]

    dataset = load_demand_dataset(records)

    # -------------------------------
    # 3. Train a forecasting model
    # -------------------------------
    feature_rows = build_feature_rows_for_dataset(dataset)
    model, _ = run_linear_regression_training(feature_rows)

    # -------------------------------
    # 4. Choose one coherent SKU-location
    #    from the demand history
    # -------------------------------
    first_row = demand_df.iloc[0]
    sku_id = first_row["sku_id"]
    location_id = first_row["location_id"]

    # -------------------------------
    # 5. Build forecast tool input
    # -------------------------------
    forecast_input = build_forecast_tool_input(
        demand_history=demand_df,
        model=model,
        sku_id=sku_id,
        location_id=location_id,
        horizon=3,
    )

    # -------------------------------
    # 6. Derive an aligned demand signal
    #    from the same SKU-location history
    # -------------------------------
    entity_history = demand_df[
        (demand_df["sku_id"] == sku_id)
        & (demand_df["location_id"] == location_id)
    ].copy()

    if entity_history.empty:
        raise ValueError(
            f"No demand history found for sku_id={sku_id}, location_id={location_id}"
        )

    expected_daily_demand = float(entity_history["units_sold"].mean())

    # -------------------------------
    # 7. Build sample network and find
    #    matching inventory record
    # -------------------------------
    network = build_sample_network()

    matching_inventory_record = next(
        (
            record
            for record in network.inventory
            if record.sku_id == sku_id and record.location_id == location_id
        ),
        None,
    )

    if matching_inventory_record is None:
        raise ValueError(
            f"No inventory record found for sku_id={sku_id}, location_id={location_id}"
        )

    # -------------------------------
    # 8. Build inventory input
    # -------------------------------
    inventory_input = InventoryStatusToolInput(
        record=matching_inventory_record,
        expected_daily_demand=expected_daily_demand,
        lead_time_days=5,
    )

    # -------------------------------
    # 9. Build replenishment input
    # -------------------------------
    replenishment_input = ReplenishmentToolInput(
        replenishment_input=ReplenishmentInput(
            sku_id=matching_inventory_record.sku_id,
            location_id=matching_inventory_record.location_id,
            inventory_position=(
                matching_inventory_record.on_hand + matching_inventory_record.on_order
            ),
            expected_daily_demand=expected_daily_demand,
            lead_time_days=5,
            safety_stock=20.0,
        )
    )

    # -------------------------------
    # 10. Run coordinator
    # -------------------------------
    decision_input = DecisionCoordinatorInput(
        forecast_input=forecast_input,
        inventory_input=inventory_input,
        replenishment_input=replenishment_input,
    )

    result = run_supply_chain_decision(decision_input)

    # -------------------------------
    # 11. Print results
    # -------------------------------
    print("\n--- FORECAST ---")
    print(result.forecast_result)

    print("\n--- INVENTORY ---")
    print(result.inventory_result)

    print("\n--- REPLENISHMENT ---")
    print(result.replenishment_result)

    print("\n--- TRACE ---")
    for step in result.execution_trace:
        print(f"{step.step_name} -> {step.tool_name}")


if __name__ == "__main__":
    main()