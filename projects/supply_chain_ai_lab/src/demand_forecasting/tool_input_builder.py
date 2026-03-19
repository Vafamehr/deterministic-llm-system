from __future__ import annotations

from typing import Any

import pandas as pd

from demand_forecasting.schemas import DemandRecord
from tools.schemas import ForecastToolInput


def build_forecast_tool_input(
    demand_history: pd.DataFrame,
    model: Any,
    sku_id: str,
    location_id: str,
    horizon: int = 1,
) -> ForecastToolInput:
    """
    Build ForecastToolInput for one SKU-location series from demand history.

    This converts DataFrame-based historical demand into the single-series
    dataclass structure expected by the forecast tool layer.
    """
    series_df = demand_history[
        (demand_history["sku_id"] == sku_id)
        & (demand_history["location_id"] == location_id)
    ].copy()

    if series_df.empty:
        raise ValueError(
            f"No demand history found for sku_id={sku_id}, location_id={location_id}"
        )

    series_df = series_df.sort_values("date").reset_index(drop=True)

    series_records = [
        DemandRecord(
            sku_id=row["sku_id"],
            location_id=row["location_id"],
            date=row["date"].date() if hasattr(row["date"], "date") else row["date"],
            demand=float(row["units_sold"]),
        )
        for _, row in series_df.iterrows()
    ]

    return ForecastToolInput(
        model=model,
        series_records=series_records,
        horizon=horizon,
    )