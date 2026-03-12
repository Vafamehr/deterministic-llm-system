# projects/supply_chain_ai_lab/src/tools/forecast_tool.py

from __future__ import annotations

from datetime import date

from demand_forecasting.service import (
    get_forecast_horizon,
    get_next_step_forecast,
)
from demand_forecasting.schemas import DemandRecord

from .schemas import ForecastToolInput, ForecastToolOutput


def get_forecast(input_data: ForecastToolInput) -> ForecastToolOutput:
    """
    Tool wrapper for the demand forecasting subsystem.

    This tool adapts the current forecasting service layer into a stable
    tool contract that future coordinators or agents can call.
    """

    if not input_data.series_records:
        raise ValueError("series_records must not be empty.")

    first_record: DemandRecord = input_data.series_records[0]

    if input_data.horizon == 1:
        predicted_values = [
            get_next_step_forecast(
                model=input_data.model,
                series_records=input_data.series_records,
            )
        ]
    else:
        predicted_values = get_forecast_horizon(
            model=input_data.model,
            series_records=input_data.series_records,
            horizon=input_data.horizon,
        )

    return ForecastToolOutput(
        sku_id=first_record.sku_id,
        location_id=first_record.location_id,
        horizon=input_data.horizon,
        predicted_values=predicted_values,
        model_name=type(input_data.model).__name__,
        generated_for_date=date.today(),
    )