
from collections import defaultdict
from typing import Dict, List, Tuple
from .schemas import DemandRecord, DemandDataset

def load_demand_dataset(records: List[DemandRecord]) -> DemandDataset:
    """
    Creates a DemandDataset from a list of DemandRecord objects.

    Ensures records are sorted chronologically.
    """

    records_sorted = sorted(records, key=lambda r: (r.sku_id, r.location_id, r.date))

    return DemandDataset(records=records_sorted)


def split_into_series(dataset: DemandDataset) -> Dict[Tuple[str, str], List[DemandRecord]]:
    """
    Groups demand records into item-location time series.

    Returns:
        Dict where key = (sku_id, location_id)
        and value = ordered list of DemandRecord
    """

    series = defaultdict(list)

    for record in dataset.records:
        key = (record.sku_id, record.location_id)
        series[key].append(record)

    # enforce chronological order
    for key in series:
        series[key].sort(key=lambda r: r.date)

    return dict(series)


def generate_history_slices(series: List[DemandRecord]) -> List[List[DemandRecord]]:
    """
    Generate rolling historical slices for forecasting evaluation.

    Example:

    [10,12,11,15] →

    [
        [10],
        [10,12],
        [10,12,11]
    ]
    """

    if len(series) < 2:
        raise ValueError("Series must contain at least two observations")

    slices = []

    for i in range(1, len(series)):
        slices.append(series[:i])

    return slices


def train_test_split_series(series, test_size: int):
    """
    Split a time series into train and test segments.

    Example:

    series = [10,12,11,15,16,18]
    test_size = 2

    train = [10,12,11,15]
    test  = [16,18]
    """

    if test_size <= 0:
        raise ValueError("test_size must be positive")

    if len(series) <= test_size:
        raise ValueError("Series too short for requested test_size")

    train = series[:-test_size]
    test = series[-test_size:]

    return train, test



