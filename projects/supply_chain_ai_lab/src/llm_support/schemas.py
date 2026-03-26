from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ExplanationTask(str, Enum):
    SIMULATION_SUMMARY = "simulation_summary"
    SCENARIO_COMPARISON = "scenario_comparison"
    RISK_EXPLANATION = "risk_explanation"


@dataclass(frozen=True)
class ScenarioExplanationRow:
    scenario_name: str
    reorder: bool
    recommended_units: float
    delta_vs_baseline: float
    days_of_supply: float
    stockout_risk: str
    inventory_pressure: str
    overstock_risk: str


@dataclass(frozen=True)
class ExplanationContext:
    baseline_reorder: bool
    baseline_recommended_units: float
    baseline_days_of_supply: float
    baseline_stockout_risk: str
    baseline_inventory_pressure: str
    baseline_overstock_risk: str
    scenario_rows: List[ScenarioExplanationRow] = field(default_factory=list)
    system_note: Optional[str] = None


@dataclass(frozen=True)
class ExplanationRequest:
    task: ExplanationTask
    context: ExplanationContext


@dataclass(frozen=True)
class ExplanationResponse:
    task: ExplanationTask
    explanation_text: str


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    issues: List[str] = field(default_factory=list)