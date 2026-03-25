from __future__ import annotations

from llm_support.schemas import ExplanationRequest, ValidationResult


def validate_explanation(
    explanation_text: str,
    request: ExplanationRequest,
) -> ValidationResult:
    issues = []

    if explanation_text is None or not explanation_text.strip():
        issues.append("Empty explanation.")
        return ValidationResult(
            is_valid=False,
            issues=issues,
        )

    cleaned_text = explanation_text.strip()
    word_count = len(cleaned_text.split())

    if word_count < 8:
        issues.append("Explanation is too short to be useful.")

    if word_count > 220:
        issues.append("Explanation is too long and may be rambling.")

    return ValidationResult(
        is_valid=len(issues) == 0,
        issues=issues,
    )