from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ScenarioComparisonRow:
    """
    One comparison row for a single scenario against the baseline scenario.

    Fields
    ------
    scenario_name:
        Name of the scenario being evaluated (for example: baseline, demand_spike).
    reorder:
        Whether the system recommends a reorder under this scenario.
    recommended_units:
        Recommended reorder quantity for this scenario.
    delta_vs_baseline:
        Difference in recommended units relative to baseline.
        Positive means more units than baseline.
        Negative means fewer units than baseline.
    """
    scenario_name: str
    reorder: bool
    recommended_units: float
    delta_vs_baseline: float


@dataclass(frozen=True)
class ScenarioAnalysisResult:
    """
    Structured output of scenario analysis.

    Fields
    ------
    baseline_scenario_name:
        The scenario used as the comparison anchor.
    comparison_rows:
        Ordered list of scenario comparison rows.
    """
    baseline_scenario_name: str
    comparison_rows: List[ScenarioComparisonRow]