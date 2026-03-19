"""
Forecast output schema definition.

This defines the contract between:
- forecasting module (ML / analytical side)
- downstream supply chain modules (operational side)
"""

FORECAST_OUTPUT_COLUMNS = [
    "sku_id",
    "location_id",
    "forecast_date",
    "forecast_units",
    "forecast_model",
    "generation_date",
]