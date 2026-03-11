from collections import defaultdict
from typing import Dict, List, Tuple

from .schemas import DemandRecord, DemandDataset


def load_demand_dataset(records: List[DemandRecord]) -> DemandDataset:
    """
    Build a DemandDataset from raw demand records.

    Records are sorted by:
    - sku_id
    - location_id
    - date
    """

    records_sorted = sorted(
        records,
        key=lambda r: (r.sku_id, r.location_id, r.date),
    )

    return DemandDataset(records=records_sorted)


def split_into_series(
    dataset: DemandDataset,
) -> Dict[Tuple[str, str], List[DemandRecord]]:
    """
    Split a dataset into ordered SKU-location demand series.

    Returns
    -------
    Dict[Tuple[str, str], List[DemandRecord]]
        Key   = (sku_id, location_id)
        Value = chronologically ordered demand records
    """

    series_map: Dict[Tuple[str, str], List[DemandRecord]] = defaultdict(list)

    for record in dataset.records:
        key = (record.sku_id, record.location_id)
        series_map[key].append(record)

    for key in series_map:
        series_map[key].sort(key=lambda r: r.date)

    return dict(series_map)


def generate_history_slices(series: List[DemandRecord]) -> List[List[DemandRecord]]:
    """
    Generate rolling historical slices for sequential forecasting evaluation.

    Example
    -------
    [10, 12, 11, 15] ->

    [
        [10],
        [10, 12],
        [10, 12, 11],
    ]
    """

    if len(series) < 2:
        raise ValueError("Series must contain at least two observations.")

    history_slices: List[List[DemandRecord]] = []

    for i in range(1, len(series)):
        history_slices.append(series[:i])

    return history_slices


def train_test_split_series(
    series: List[DemandRecord],
    test_size: int,
) -> Tuple[List[DemandRecord], List[DemandRecord]]:
    """
    Split one time series into train and test segments.

    Example
    -------
    series = [10, 12, 11, 15, 16, 18]
    test_size = 2

    train = [10, 12, 11, 15]
    test  = [16, 18]
    """

    if test_size <= 0:
        raise ValueError("test_size must be positive.")

    if len(series) <= test_size:
        raise ValueError("Series is too short for the requested test_size.")

    train = series[:-test_size]
    test = series[-test_size:]

    return train, test