
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



