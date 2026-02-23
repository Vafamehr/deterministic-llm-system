from enum import Enum

# It’s an Enum class.

class AgentAction(str, Enum):
    STOP = "stop"
    RUN_DETERMINISTIC = "run_deterministic"
    RUN_LLM = "run_llm"
    RUN_CROSS_CHECK = "run_cross_check"
    
    

