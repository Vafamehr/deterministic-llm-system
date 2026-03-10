from typing import List, Dict
from .schemas import DemandRecord, DemandDataset, ForecastFeatureRow, ForecastPredictionRow
import pandas as pd
from datetime import date, timedelta


def create_lag_features(series: List[DemandRecord], lag: int = 1) -> List[Dict]:
    """
    Generates lag features for a demand series.

    Returns a list of dictionaries where each row contains:
    - date
    - demand
    - lag_1, lag_2, ... depending on lag parameter
    """

    rows = []

    for i in range(lag, len(series)):
        row = {
            "date": series[i].date,
            "demand": series[i].demand,
        }

        for lag_step in range(1, lag + 1):
            row[f"lag_{lag_step}"] = series[i - lag_step].demand

        rows.append(row)

    return rows


def create_rolling_mean_feature(series: List[DemandRecord], window: int = 3) -> List[Dict]:
    """
    Generates rolling mean features for a demand series.

    Returns a list of dictionaries where each row contains:
    - date
    - demand
    - rolling_mean_{window}
    """

    rows = []

    for i in range(window, len(series)):
        history = [series[j].demand for j in range(i - window, i)]

        row = {
            "date": series[i].date,
            "demand": series[i].demand,
            f"rolling_mean_{window}": sum(history) / window,
        }

        rows.append(row)

    return rows


def build_feature_rows_for_series(
    series: List[DemandRecord],
    lag_steps: List[int] = [1, 2],
    rolling_windows: List[int] = [3],
) -> List[ForecastFeatureRow]:
    """
    Convert one ordered demand series into model-ready feature rows.

    Parameters
    ----------
    series : List[DemandRecord]
        Time-ordered demand history for one sku-location pair

    lag_steps : List[int]
        Lag offsets to include, e.g. [1, 2, 7]

    rolling_windows : List[int]
        Rolling mean window sizes to include, e.g. [3, 7]

    Returns
    -------
    List[ForecastFeatureRow]
    """

    rows: List[ForecastFeatureRow] = []

    max_lag = max(lag_steps) if lag_steps else 0
    max_window = max(rolling_windows) if rolling_windows else 0
    min_index = max(max_lag, max_window)

    for i in range(min_index, len(series)):
        current = series[i]
        feature_dict: Dict[str, float] = {}

        # dynamic lag features
        for lag in lag_steps:
            feature_dict[f"lag_{lag}"] = float(series[i - lag].demand)

        # dynamic rolling mean features
        for window in rolling_windows:
            history = [series[j].demand for j in range(i - window, i)]
            feature_dict[f"rolling_mean_{window}"] = float(sum(history) / window)

        row = ForecastFeatureRow(
            sku_id=current.sku_id,
            location_id=current.location_id,
            date=current.date,
            features=feature_dict,
            target=float(current.demand),
        )

        rows.append(row)

    return rows


def build_feature_rows_for_dataset(
    dataset: DemandDataset,
    lag_steps: List[int] = [1, 2],
    rolling_windows: List[int] = [3],
) -> List[ForecastFeatureRow]:
    """
    Build model-ready feature rows across the full dataset.

    Flow:
        dataset -> segmented series -> feature rows per series -> combined rows
    """

    from .data import split_into_series

    all_rows: List[ForecastFeatureRow] = []

    series_map = split_into_series(dataset)

    for _, series in series_map.items():
        series_rows = build_feature_rows_for_series(
            series=series,
            lag_steps=lag_steps,
            rolling_windows=rolling_windows,
        )
        all_rows.extend(series_rows)

    return all_rows


def feature_rows_to_dataframe(rows: List[ForecastFeatureRow]) -> pd.DataFrame:
    """
    Convert feature row dataclasses into a flat pandas DataFrame.
    """

    flattened_rows = []

    for row in rows:
        output_row = {
            "sku_id": row.sku_id,
            "location_id": row.location_id,
            "date": row.date,
            "target": row.target,
        }
        output_row.update(row.features)
        flattened_rows.append(output_row)

    return pd.DataFrame(flattened_rows)


def build_prediction_row_for_series(
    series: List[DemandRecord],
    lag_steps: List[int] = [1, 2],
    rolling_windows: List[int] = [3],
) -> ForecastPredictionRow:
    """
    Build one prediction feature row for the next time step of a single series.
    """

    if not series:
        raise ValueError("Series is empty.")

    max_lag = max(lag_steps) if lag_steps else 0
    max_window = max(rolling_windows) if rolling_windows else 0
    required_history = max(max_lag, max_window)

    if len(series) < required_history:
        raise ValueError(
            f"Not enough history to build prediction row. "
            f"Need at least {required_history} records, got {len(series)}."
        )

    last_record = series[-1]
    feature_dict: Dict[str, float] = {}

    for lag in lag_steps:
        feature_dict[f"lag_{lag}"] = float(series[-lag].demand)

    for window in rolling_windows:
        history = [record.demand for record in series[-window:]]
        feature_dict[f"rolling_mean_{window}"] = float(sum(history) / window)

    return ForecastPredictionRow(
        sku_id=last_record.sku_id,
        location_id=last_record.location_id,
        prediction_date=last_record.date + timedelta(days=1),
        features=feature_dict,
    )


def prediction_row_to_dataframe(row: ForecastPredictionRow) -> pd.DataFrame:
    """
    Convert one prediction row into a flat pandas DataFrame.
    """

    output_row = {
        "sku_id": row.sku_id,
        "location_id": row.location_id,
        "prediction_date": row.prediction_date,
    }
    output_row.update(row.features)

    return pd.DataFrame([output_row])