from dataclasses import dataclass
from typing import List, Optional

from decision_intelligence.schemas import DecisionIntelligenceOutput


@dataclass(frozen=True)
class ScenarioComparisonRow:
    """
    One comparison row for a single scenario against the baseline scenario.
    """
    scenario_name: str
    reorder: bool
    recommended_units: float
    delta_vs_baseline: float
    days_of_supply: float
    stockout_risk: str
    inventory_pressure: str
    overstock_risk: str
    decision_intelligence: Optional[DecisionIntelligenceOutput] = None


@dataclass(frozen=True)
class ScenarioAnalysisResult:
    """
    Structured output of scenario analysis.
    """
    baseline_scenario_name: str
    comparison_rows: List[ScenarioComparisonRow]