from __future__ import annotations

from router.strategy import Strategy


def route(user_input: str) -> Strategy:
    text = (user_input or "").lower()

    # Priority order: strongest intent first
    if "summarize" in text:
        return Strategy.SUMMARY


    if "escalate" in text or "should we" in text:
        return Strategy.POLICY

    if "delay" in text or "metric" in text:
        return Strategy.ANALYTICS

    return Strategy.GENERAL