from dataclasses import dataclass
from typing import Optional


@dataclass
class ExecutionPlan:
    run_deterministic: bool
    run_llm: bool
    run_cross_check: bool
    use_tool: Optional[str] = None