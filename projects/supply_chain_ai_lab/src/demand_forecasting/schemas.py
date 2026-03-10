from dataclasses import dataclass
from datetime import date
from typing import List, Dict

@dataclass
class DemandRecord:
    sku_id: str
    location_id: str
    date: date
    demand: float



@dataclass
class DemandDataset:
    records: List[DemandRecord]




@dataclass
class ForecastFeatureRow:
    sku_id: str
    location_id: str
    date: date
    features: Dict[str, float]
    target: float      