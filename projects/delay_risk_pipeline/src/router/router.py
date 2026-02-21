from __future__ import annotations

from .rules import route
from .strategy import Strategy


def dispatch(user_input: str) -> Strategy:
    return route(user_input)