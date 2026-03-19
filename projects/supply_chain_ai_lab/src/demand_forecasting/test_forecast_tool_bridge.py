from pathlib import Path

from demand_forecasting.data_loader import load_demand_history
from demand_forecasting.features import build_feature_rows_for_series
from demand_forecasting.model import run_linear_regression_training, run_xgboost_training
from demand_forecasting.tool_input_builder import build_forecast_tool_input
from tools.forecast_tool import get_forecast


def main() -> None:
    src_root = Path(__file__).resolve().parents[1]
    csv_path = src_root / "sample_data" / "synthetic_demand_history.csv"

    demand_df = load_demand_history(csv_path)

    first_row = demand_df.iloc[0]
    sku_id = first_row["sku_id"]
    location_id = first_row["location_id"]

    tool_input = build_forecast_tool_input(
        demand_history=demand_df,
        model=None,
        sku_id=sku_id,
        location_id=location_id,
        horizon=3,
    )

    feature_rows = build_feature_rows_for_series(tool_input.series_records)
    # model, _ = run_linear_regression_training(feature_rows)
    model, _ = run_xgboost_training(feature_rows)
    

    tool_input = build_forecast_tool_input(
        demand_history=demand_df,
        model=model,
        sku_id=sku_id,
        location_id=location_id,
        horizon=3,
    )

    forecast_output = get_forecast(tool_input)

    print("Forecast tool bridge test succeeded.")
    print(f"sku_id: {forecast_output.sku_id}")
    print(f"location_id: {forecast_output.location_id}")
    print(f"horizon: {forecast_output.horizon}")
    print(f"predicted_values: {forecast_output.predicted_values}")
    print(f"model_name: {forecast_output.model_name}")
    print(f"generated_for_date: {forecast_output.generated_for_date}")


if __name__ == "__main__":
    main()