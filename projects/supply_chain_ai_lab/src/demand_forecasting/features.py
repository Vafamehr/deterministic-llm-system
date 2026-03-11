from datetime import timedelta
from typing import Dict, List, Optional

import pandas as pd

from .schemas import (
    DemandDataset,
    DemandRecord,
    ForecastFeatureRow,
    ForecastPredictionRow,
)


def create_lag_features(series: List[DemandRecord], lag: int = 1) -> List[Dict]:
    """
    Generate simple lag features for a demand series.

    Returns a list of dictionaries with:
    - date
    - demand
    - lag_1, lag_2, ..., lag_k
    """

    rows: List[Dict] = []

    for i in range(lag, len(series)):
        row = {
            "date": series[i].date,
            "demand": series[i].demand,
        }

        for lag_step in range(1, lag + 1):
            row[f"lag_{lag_step}"] = series[i - lag_step].demand

        rows.append(row)

    return rows


def create_rolling_mean_feature(
    series: List[DemandRecord],
    window: int = 3,
) -> List[Dict]:
    """
    Generate rolling mean features for a demand series.

    Returns a list of dictionaries with:
    - date
    - demand
    - rolling_mean_{window}
    """

    rows: List[Dict] = []

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
    lag_steps: Optional[List[int]] = None,
    rolling_windows: Optional[List[int]] = None,
) -> List[ForecastFeatureRow]:
    """
    Convert one ordered demand series into model-ready training rows.

    Parameters
    ----------
    series : List[DemandRecord]
        Time-ordered demand history for one SKU-location pair

    lag_steps : Optional[List[int]]
        Lag offsets to include, e.g. [1, 2, 7]

    rolling_windows : Optional[List[int]]
        Rolling mean window sizes to include, e.g. [3, 7]

    Returns
    -------
    List[ForecastFeatureRow]
    """

    lag_steps = lag_steps or [1, 2]
    rolling_windows = rolling_windows or [3]

    rows: List[ForecastFeatureRow] = []

    max_lag = max(lag_steps) if lag_steps else 0
    max_window = max(rolling_windows) if rolling_windows else 0
    min_index = max(max_lag, max_window)

    for i in range(min_index, len(series)):
        current = series[i]
        feature_dict: Dict[str, float] = {}

        for lag in lag_steps:
            feature_dict[f"lag_{lag}"] = float(series[i - lag].demand)

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
    lag_steps: Optional[List[int]] = None,
    rolling_windows: Optional[List[int]] = None,
) -> List[ForecastFeatureRow]:
    """
    Build model-ready feature rows across the full dataset.

    Flow:
        dataset -> segmented series -> feature rows per series -> combined rows
    """

    from .data import split_into_series

    lag_steps = lag_steps or [1, 2]
    rolling_windows = rolling_windows or [3]

    all_rows: List[ForecastFeatureRow] = []

    series_map = split_into_series(dataset)

    for series in series_map.values():
        series_rows = build_feature_rows_for_series(
            series=series,
            lag_steps=lag_steps,
            rolling_windows=rolling_windows,
        )
        all_rows.extend(series_rows)

    return all_rows


def feature_rows_to_dataframe(rows: List[ForecastFeatureRow]) -> pd.DataFrame:
    """
    Convert training feature rows into a flat pandas DataFrame.
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
    lag_steps: Optional[List[int]] = None,
    rolling_windows: Optional[List[int]] = None,
) -> ForecastPredictionRow:
    """
    Build one prediction feature row for the next time step of a single series.
    """

    lag_steps = lag_steps or [1, 2]
    rolling_windows = rolling_windows or [3]

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