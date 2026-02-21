from enum import Enum

class Strategy(str, Enum):
    ANALYTICS = "analytics"
    POLICY = "policy"
    SUMMARY = "summary"
    GENERAL = "general"