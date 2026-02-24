from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime


@dataclass
class TraceEvent:
    step: str
    status: str
    reason: str
    data_snapshot: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class DecisionTrace:
    events: List[TraceEvent] = field(default_factory=list)

    def add_event(self, step: str, status: str, reason: str, data_snapshot: Dict[str, Any]):
        self.events.append(
            TraceEvent(
                step=step,
                status=status,
                reason=reason,
                data_snapshot=data_snapshot
            )
        )

    def to_dict(self):
        return [event.__dict__ for event in self.events]