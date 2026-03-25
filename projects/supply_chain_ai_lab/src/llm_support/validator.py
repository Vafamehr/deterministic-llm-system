from __future__ import annotations

from llm_support.schemas import ExplanationRequest, ValidationResult


def _validate_common(explanation_text: str, request: ExplanationRequest) -> list[str]:
    issues: list[str] = []

    cleaned_text = explanation_text.strip()
    lowered_text = cleaned_text.lower()

    if not cleaned_text:
        issues.append("Explanation text is empty.")
        return issues

    if len(cleaned_text) < 20:
        issues.append("Explanation text is too short to be useful.")

    scenario_names = [row.scenario_name.lower() for row in request.context.scenario_rows]
    if scenario_names and not any(name in lowered_text for name in scenario_names):
        issues.append("Explanation does not reference any known scenario name.")

    return issues


def _validate_simulation_summary(
    explanation_text: str,
    request: ExplanationRequest,
) -> list[str]:
    return []


def _validate_scenario_comparison(
    explanation_text: str,
    request: ExplanationRequest,
) -> list[str]:
    issues: list[str] = []
    lowered_text = explanation_text.lower()

    if "baseline" not in lowered_text:
        issues.append("Scenario comparison should reference the baseline scenario.")

    return issues


def _validate_risk_explanation(
    explanation_text: str,
    request: ExplanationRequest,
) -> list[str]:
    issues: list[str] = []
    lowered_text = explanation_text.lower()

    if not any(
        phrase in lowered_text
        for phrase in ["days of supply", "stockout risk", "inventory pressure"]
    ):
        issues.append(
            "Risk explanation must reference at least one key risk signal "
            "(days of supply, stockout risk, or inventory pressure)."
        )

    return issues


def validate_explanation(
    explanation_text: str,
    request: ExplanationRequest,
) -> ValidationResult:
    issues = _validate_common(explanation_text=explanation_text, request=request)

    if request.task == "simulation_summary":
        issues.extend(
            _validate_simulation_summary(
                explanation_text=explanation_text,
                request=request,
            )
        )
    elif request.task == "scenario_comparison":
        issues.extend(
            _validate_scenario_comparison(
                explanation_text=explanation_text,
                request=request,
            )
        )
    elif request.task == "risk_explanation":
        issues.extend(
            _validate_risk_explanation(
                explanation_text=explanation_text,
                request=request,
            )
        )
    else:
        issues.append(f"Unsupported explanation task: {request.task}")

    return ValidationResult(
        is_valid=len(issues) == 0,
        issues=issues,
    )