from __future__ import annotations

from router.rules import route
from router.strategy import Strategy


def choose_branch(user_input: str) -> Strategy:
    return route(user_input)