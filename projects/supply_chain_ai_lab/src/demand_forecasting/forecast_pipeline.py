from __future__ import annotations

from pathlib import Path

import pandas as pd

from demand_forecasting.data_loader import load_demand_history
from demand_forecasting.forecast_schema import FORECAST_OUTPUT_COLUMNS


def generate_naive_forecast(
    demand_history: pd.DataFrame,
    forecast_horizon_days: int = 7,
    forecast_model: str = "naive_last_value",
) -> pd.DataFrame:
    """
    Generate a simple baseline forecast using the last observed demand value
    for each (sku_id, location_id) pair.

    Output schema follows FORECAST_OUTPUT_COLUMNS.
    """
    required_columns = ["date", "sku_id", "location_id", "units_sold"]
    missing_columns = [
        column for column in required_columns if column not in demand_history.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Demand history is missing required columns: {missing_columns}"
        )

    latest_history = (
        demand_history.sort_values(["sku_id", "location_id", "date"])
        .groupby(["sku_id", "location_id"], as_index=False)
        .tail(1)
        .copy()
    )

    max_history_date = demand_history["date"].max()

    generation_date = pd.Timestamp(max_history_date).normalize()
    # keeps pandas type
    # removes time
    # safe for joins, merges, grouping

    forecast_rows = []

    for _, row in latest_history.iterrows():
        for day_offset in range(1, forecast_horizon_days + 1):
            forecast_rows.append(
                {
                    "sku_id": row["sku_id"],
                    "location_id": row["location_id"],
                    "forecast_date": generation_date + pd.Timedelta(days=day_offset),
                    "forecast_units": float(row["units_sold"]),
                    "forecast_model": forecast_model,
                    "generation_date": generation_date,
                }
            )

    forecast_df = pd.DataFrame(forecast_rows)
    forecast_df = forecast_df[FORECAST_OUTPUT_COLUMNS].copy()

    return forecast_df



def run_forecast_pipeline(
    csv_path: str | Path,
    forecast_horizon_days: int = 7,
) -> pd.DataFrame:
    """
    End-to-end forecasting entrypoint.

    Flow:
    load demand → generate forecast → return forecast DataFrame
    """
    csv_path = Path(csv_path)

    demand_df = load_demand_history(csv_path)

    forecast_df = generate_naive_forecast(
        demand_df,
        forecast_horizon_days=forecast_horizon_days,
    )

    return forecast_df


