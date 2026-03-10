from typing import List
from .schemas import DemandRecord

from typing import Dict, Tuple
from .schemas import DemandDataset
from .data import split_into_series


def naive_forecast(series: List[DemandRecord]) -> float:
    """
    Naive forecast baseline.

    Forecast rule:
        next demand = last observed demand
    """

    if not series:
        raise ValueError("Series is empty")

    last_record = series[-1]
    return float(last_record.demand)


def mean_absolute_error(actual: List[float], predicted: List[float]) -> float:
    """
    Computes Mean Absolute Error (MAE).
    """

    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length")

    if not actual:
        raise ValueError("actual and predicted cannot be empty")

    absolute_errors = [abs(a - p) for a, p in zip(actual, predicted)]

    return sum(absolute_errors) / len(absolute_errors)

def evaluate_naive_on_series(series: List[DemandRecord]) -> float:
    """
    Evaluates the naive forecast on a single time series.

    The naive forecast predicts the next demand using the
    last observed demand.
    """

    if len(series) < 2:
        raise ValueError("Series must contain at least two observations")

    actual = []
    predicted = []

    for i in range(1, len(series)):
        history = series[:i]

        prediction = naive_forecast(history)

        predicted.append(prediction)
        actual.append(series[i].demand)

    return mean_absolute_error(actual, predicted) 



def evaluate_naive_on_dataset(dataset: DemandDataset) -> Dict[Tuple[str, str], float]:
    """
    Evaluate the naive forecast across all SKU-location series.

    Returns a dictionary mapping:
    (sku_id, location_id) -> MAE
    """

    series_map = split_into_series(dataset)

    results = {}

    for key, series in series_map.items():

        if len(series) < 2:
            continue

        mae = evaluate_naive_on_series(series)

        results[key] = mae

    return results 


def mean_mae_across_series(results: dict) -> float:
    """
    Compute the mean MAE across all evaluated series.
    """

    if not results:
        raise ValueError("results cannot be empty")

    return sum(results.values()) / len(results)