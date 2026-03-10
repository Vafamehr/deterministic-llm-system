from typing import List
from .schemas import ForecastFeatureRow


def naive_forecast_last_value(rows: List[ForecastFeatureRow]) -> List[float]:
    """
    Naive forecast baseline.

    Prediction rule:
        forecast = lag_1

    This assumes the next demand will equal the most recent observed demand.
    """

    predictions: List[float] = []

    for row in rows:
        pred = row.features.get("lag_1", 0.0)
        predictions.append(pred)

    return predictions