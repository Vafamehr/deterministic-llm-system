from typing import List
from .schemas import DemandRecord


def naive_forecast(series: List[DemandRecord]) -> float:
    """
    Returns the naive forecast for the next period.

    The naive forecast equals the last observed demand.
    """

    if not series:
        raise ValueError("Series is empty")

    last_record = series[-1]

    return last_record.demand


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