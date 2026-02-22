from dataclasses import dataclass
from typing import Any, Optional

from stage_status import StageStatus


@dataclass
class StageResult:
    status: StageStatus
    data: Optional[Any]
    error: Optional[str]
    latency_ms: float