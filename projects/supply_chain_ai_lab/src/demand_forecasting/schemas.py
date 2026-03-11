from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Tuple


@dataclass
class DemandRecord:
    """
    One observed demand data point for a SKU at a location on a specific date.
    """
    sku_id: str
    location_id: str
    date: date
    demand: float


@dataclass
class DemandDataset:
    """
    Container for a collection of demand records.
    """
    records: List[DemandRecord]


@dataclass
class ForecastFeatureRow:
    """
    Model-ready training row built from historical demand.

    - features: lag / rolling statistics used by the model
    - target: actual demand to be predicted
    """
    sku_id: str
    location_id: str
    date: date
    features: Dict[str, float]
    target: float


@dataclass
class ForecastPredictionRow:
    """
    Feature row used for prediction (no target value available).
    """
    sku_id: str
    location_id: str
    prediction_date: date
    features: Dict[str, float]


@dataclass
class ForecastEvaluationResult:
    """
    Evaluation summary across multiple SKU-location series.
    """
    per_series_mae: Dict[Tuple[str, str], float]
    mean_mae: float
    series_count: int