from __future__ import annotations

from dataclasses import dataclass

from disruption_modeling.schemas import DisruptionImpact, DisruptionScenario


@dataclass(frozen=True)
class ResolvedDisruption:
    scenario_name: str
    impact: DisruptionImpact


def resolve_disruption(
    disruption_scenario: DisruptionScenario,
) -> ResolvedDisruption:
    """
    Resolve a business disruption scenario into operational impacts
    that downstream modules can consume deterministically.
    """
    return ResolvedDisruption(
        scenario_name=disruption_scenario.scenario_name,
        impact=disruption_scenario.impact,
    )