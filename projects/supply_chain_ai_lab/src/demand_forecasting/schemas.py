from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Tuple

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


@dataclass
class ForecastPredictionRow:
    sku_id: str
    location_id: str
    prediction_date: date
    features: Dict[str, float]  




@dataclass
class ForecastEvaluationResult:
    per_series_mae: Dict[Tuple[str, str], float]
    mean_mae: float
    series_count: int           