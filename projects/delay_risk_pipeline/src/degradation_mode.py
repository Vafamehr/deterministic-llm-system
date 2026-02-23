from enum import Enum


class DegradationMode(str, Enum):
    NONE = "NONE"
    DETERMINISTIC_ONLY = "DETERMINISTIC_ONLY"
    LLM_ONLY = "LLM_ONLY"
    NO_CROSS_CHECK = "NO_CROSS_CHECK"
    TOTAL_FAILURE = "TOTAL_FAILURE"