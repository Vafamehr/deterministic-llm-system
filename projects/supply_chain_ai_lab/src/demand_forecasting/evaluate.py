from typing import List
from typing import Dict, Tuple

from .schemas import DemandRecord
from .schemas import DemandDataset
from .schemas import ForecastEvaluationResult

from .data import generate_history_slices
from .data import train_test_split_series
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
    """

    if len(series) < 2:
        raise ValueError("Series must contain at least two observations")


    slices = generate_history_slices(series)

    actual = []
    predicted = []

    for i, history in enumerate(slices):

        prediction = naive_forecast(history)

        predicted.append(prediction)
        actual.append(series[i + 1].demand)

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




def evaluate_naive_dataset_summary(dataset: DemandDataset) -> ForecastEvaluationResult:
    """
    Evaluate the naive forecast on a dataset and return
    a structured summary result.
    """

    per_series_mae = evaluate_naive_on_dataset(dataset)
    mean_mae = mean_mae_across_series(per_series_mae)

    return ForecastEvaluationResult(
        per_series_mae=per_series_mae,
        mean_mae=mean_mae,
        series_count=len(per_series_mae),
    )


def evaluate_naive_train_test(train_series, test_series) -> float:
    """
    Evaluate naive forecasting on a held-out test horizon.

    The first prediction uses the last demand from the train series.
    Each later prediction uses the previous actual demand from the test series.
    """

    if not train_series:
        raise ValueError("train_series cannot be empty")

    if not test_series:
        raise ValueError("test_series cannot be empty")

    predicted = [train_series[-1].demand]

    for i in range(1, len(test_series)):
        predicted.append(test_series[i - 1].demand)

    actual = [record.demand for record in test_series]

    return mean_absolute_error(actual, predicted)





def evaluate_naive_series_with_split(series, test_size: int) -> float:
    """
    Run a full naive forecasting experiment on one series
    using a train/test split.
    """

    train_series, test_series = train_test_split_series(series, test_size)

    return evaluate_naive_train_test(train_series, test_series) 