from typing import Dict, List, Tuple

from .data import generate_history_slices, split_into_series, train_test_split_series
from .schemas import DemandDataset, DemandRecord, ForecastEvaluationResult


def naive_forecast(series: List[DemandRecord]) -> float:
    """
    Naive forecast baseline.

    Forecast rule:
        next demand = last observed demand
    """

    if not series:
        raise ValueError("Series is empty.")

    last_record = series[-1]
    return float(last_record.demand)


def mean_absolute_error(actual: List[float], predicted: List[float]) -> float:
    """
    Compute Mean Absolute Error (MAE).
    """

    if len(actual) != len(predicted):
        raise ValueError("actual and predicted must have the same length.")

    if not actual:
        raise ValueError("actual and predicted cannot be empty.")

    absolute_errors = [abs(a - p) for a, p in zip(actual, predicted)]

    return sum(absolute_errors) / len(absolute_errors)


def evaluate_naive_on_series(series: List[DemandRecord]) -> float:
    """
    Evaluate naive forecasting on a single full time series
    using rolling historical slices.
    """

    if len(series) < 2:
        raise ValueError("Series must contain at least two observations.")

    slices = generate_history_slices(series)

    actual: List[float] = []
    predicted: List[float] = []

    for i, history in enumerate(slices):
        prediction = naive_forecast(history)
        predicted.append(prediction)
        actual.append(float(series[i + 1].demand))

    return mean_absolute_error(actual, predicted)


def evaluate_naive_on_dataset(dataset: DemandDataset) -> Dict[Tuple[str, str], float]:
    """
    Evaluate naive forecasting across all SKU-location series.

    Returns
    -------
    Dict[Tuple[str, str], float]
        Mapping from (sku_id, location_id) to MAE
    """

    series_map = split_into_series(dataset)
    results: Dict[Tuple[str, str], float] = {}

    for key, series in series_map.items():
        if len(series) < 2:
            continue

        mae = evaluate_naive_on_series(series)
        results[key] = mae

    return results


def mean_mae_across_series(results: Dict[Tuple[str, str], float]) -> float:
    """
    Compute the mean MAE across all evaluated series.
    """

    if not results:
        raise ValueError("results cannot be empty.")

    return sum(results.values()) / len(results)


def evaluate_naive_dataset_summary(dataset: DemandDataset) -> ForecastEvaluationResult:
    """
    Evaluate naive forecasting on a dataset and return
    a structured summary result.
    """

    per_series_mae = evaluate_naive_on_dataset(dataset)
    mean_mae = mean_mae_across_series(per_series_mae)

    return ForecastEvaluationResult(
        per_series_mae=per_series_mae,
        mean_mae=mean_mae,
        series_count=len(per_series_mae),
    )


def evaluate_naive_train_test(
    train_series: List[DemandRecord],
    test_series: List[DemandRecord],
) -> float:
    """
    Evaluate naive forecasting on a held-out test horizon.

    The first prediction uses the last demand from the train series.
    Each later prediction uses the previous actual demand from the test series.
    """

    if not train_series:
        raise ValueError("train_series cannot be empty.")

    if not test_series:
        raise ValueError("test_series cannot be empty.")

    predicted = [float(train_series[-1].demand)]

    for i in range(1, len(test_series)):
        predicted.append(float(test_series[i - 1].demand))

    actual = [float(record.demand) for record in test_series]

    return mean_absolute_error(actual, predicted)


def evaluate_naive_series_with_split(
    series: List[DemandRecord],
    test_size: int,
) -> float:
    """
    Run a naive forecasting experiment on one series
    using a train/test split.
    """

    train_series, test_series = train_test_split_series(series, test_size)

    return evaluate_naive_train_test(train_series, test_series)


def evaluate_naive_dataset_with_split(
    dataset: DemandDataset,
    test_size: int,
) -> ForecastEvaluationResult:
    """
    Run naive train/test evaluation across all eligible series
    in the dataset and return a structured summary.
    """

    series_map = split_into_series(dataset)
    results: Dict[Tuple[str, str], float] = {}

    for key, series in series_map.items():
        if len(series) <= test_size:
            continue

        mae = evaluate_naive_series_with_split(series, test_size)
        results[key] = mae

    if not results:
        raise ValueError("No eligible series found for the requested test_size.")

    return ForecastEvaluationResult(
        per_series_mae=results,
        mean_mae=mean_mae_across_series(results),
        series_count=len(results),
    )


def evaluate_naive_horizon(series: List[DemandRecord], horizon: int) -> float:
    """
    Evaluate naive forecasting for a fixed forecast horizon.

    The last `horizon` observations are treated as the future
    forecast window, and earlier observations form the training history.
    """

    if horizon <= 0:
        raise ValueError("horizon must be positive.")

    if len(series) <= horizon:
        raise ValueError("Series too short for requested horizon.")

    train_series = series[:-horizon]
    test_series = series[-horizon:]

    return evaluate_naive_train_test(train_series, test_series)