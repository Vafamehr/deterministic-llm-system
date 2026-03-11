from datetime import date

from .features import build_feature_rows_for_series
from .model import run_linear_regression_training
from .schemas import DemandRecord
from .service import get_forecast_horizon, get_next_step_forecast


series = [
    DemandRecord(sku_id="A", location_id="X", date=date(2025, 1, 1), demand=10),
    DemandRecord(sku_id="A", location_id="X", date=date(2025, 1, 2), demand=12),
    DemandRecord(sku_id="A", location_id="X", date=date(2025, 1, 3), demand=11),
    DemandRecord(sku_id="A", location_id="X", date=date(2025, 1, 4), demand=13),
    DemandRecord(sku_id="A", location_id="X", date=date(2025, 1, 5), demand=14),
]

feature_rows = build_feature_rows_for_series(series)
model, predictions = run_linear_regression_training(feature_rows)

next_forecast = get_next_step_forecast(model, series)
horizon_forecast = get_forecast_horizon(model, series, horizon=3)

print("Feature rows:")
print(feature_rows)

print("\nIn-sample predictions:")
print(predictions)

print("\nNext-step forecast:")
print(next_forecast)
print(type(next_forecast))

print("\n3-step horizon forecast:")
print(horizon_forecast)
print(type(horizon_forecast))