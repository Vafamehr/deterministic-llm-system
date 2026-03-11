from typing import List

from .evaluate import evaluate_naive_dataset_with_split
from .features import build_prediction_row_for_series, prediction_row_to_dataframe
from .model import predict_with_model
from .schemas import DemandDataset, DemandRecord


def run_naive_forecast_experiment(
    dataset: DemandDataset,
    test_size: int,
):
    """
    Run the baseline naive forecasting experiment
    across the full dataset using a train/test split.
    """

    results = evaluate_naive_dataset_with_split(dataset, test_size)

    return results


def get_next_step_forecast(model, series_records: List[DemandRecord]) -> float:
    """
    Generate a one-step-ahead forecast for a single series
    using a trained model.
    """

    prediction_row = build_prediction_row_for_series(series_records)
    prediction_df = prediction_row_to_dataframe(prediction_row)

    predictions = predict_with_model(model, prediction_df)

    return float(predictions[0])


def get_forecast_horizon(
    model,
    series_records: List[DemandRecord],
    horizon: int,
) -> List[float]:
    """
    Generate a multi-step forecast recursively for a single series.

    Workflow:
    - build next-step prediction row from current history
    - predict next demand
    - append predicted demand as a synthetic future record
    - repeat until horizon is reached
    """

    if horizon <= 0:
        raise ValueError("horizon must be positive.")

    simulated_series = list(series_records)
    forecasts: List[float] = []

    for _ in range(horizon):
        prediction_row = build_prediction_row_for_series(simulated_series)
        prediction_df = prediction_row_to_dataframe(prediction_row)

        prediction = float(predict_with_model(model, prediction_df)[0])
        forecasts.append(prediction)

        simulated_series.append(
            DemandRecord(
                sku_id=prediction_row.sku_id,
                location_id=prediction_row.location_id,
                date=prediction_row.prediction_date,
                demand=prediction,
            )
        )

    return forecasts