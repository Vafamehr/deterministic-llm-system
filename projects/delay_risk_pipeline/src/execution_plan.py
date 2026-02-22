from dataclasses import dataclass


@dataclass
class ExecutionPlan:
    run_deterministic: bool
    run_llm: bool
    run_cross_check: bool