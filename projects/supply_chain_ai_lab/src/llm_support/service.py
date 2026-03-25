from __future__ import annotations

from llm_support.client import LLMClient
from llm_support.context_builder import build_explanation_context
from llm_support.prompt_builder import build_explanation_prompt
from llm_support.schemas import (
    ExplanationRequest,
    ExplanationResponse,
    ExplanationTask,
)
from llm_support.validator import validate_explanation
from simulation_engine.schemas import SimulationResult


class LLMExplanationService:
    def __init__(self, client: LLMClient | None = None) -> None:
        self.client = client or LLMClient()

    def explain(
        self,
        simulation_result: SimulationResult,
        task: ExplanationTask,
    ) -> ExplanationResponse:
        if simulation_result.analysis_result is None:
            raise ValueError(
                "Simulation result must include analysis_result before explanation."
            )

        context = build_explanation_context(
            analysis_result=simulation_result.analysis_result
        )

        request = ExplanationRequest(
            task=task,
            context=context,
        )

        prompt = build_explanation_prompt(request=request)
        explanation_text = self.client.generate(prompt=prompt)

        validation_result = validate_explanation(
            explanation_text=explanation_text,
            request=request,
        )

        if not validation_result.is_valid:
            raise ValueError(
                "Generated explanation failed validation: "
                + "; ".join(validation_result.issues)
            )

        return ExplanationResponse(
            task=task,
            explanation_text=explanation_text,
        )