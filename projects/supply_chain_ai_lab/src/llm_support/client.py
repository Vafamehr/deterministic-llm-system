from __future__ import annotations


class LLMClient:
    def __init__(self, model_name: str = "stub-llm") -> None:
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        return (
            "Baseline scenario remains the reference point for comparison. "
            "In the baseline scenario, the system establishes the starting reorder decision, "
            "recommended units, days of supply, stockout risk, and inventory pressure. "
            "Compared with baseline, the demand_spike scenario increases recommended units and "
            "indicates tighter inventory conditions. "
            "Compared with baseline, the supplier_delay scenario also increases recommended units "
            "and reflects operational risk driven by delayed replenishment. "
            "Overall, baseline is the anchor, while demand_spike and supplier_delay show higher risk "
            "and greater replenishment need."
        )