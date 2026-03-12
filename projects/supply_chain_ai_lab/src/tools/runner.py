from __future__ import annotations

from typing import Union

from .forecast_tool import get_forecast
from .inventory_tool import get_inventory_status
from .replenishment_tool import get_replenishment_recommendation_tool
from .schemas import (
    ForecastToolInput,
    ForecastToolOutput,
    InventoryStatusToolInput,
    InventoryStatusToolOutput,
    ReplenishmentToolInput,
    ReplenishmentToolOutput,
)


## allowed tool requests: So either of these only acceptable. Anything else is rejected.
ToolInput = Union[
    ForecastToolInput,
    InventoryStatusToolInput,
    ReplenishmentToolInput,
]

ToolOutput = Union[
    ForecastToolOutput,
    InventoryStatusToolOutput,
    ReplenishmentToolOutput,
]


def run_tool(tool_name: str, input_data: ToolInput) -> ToolOutput:
    """
    Dynamically execute a tool by name.

    Supported tools:
    - forecast
    - inventory_status
    - replenishment
    """

    if tool_name == "forecast":
        if not isinstance(input_data, ForecastToolInput):
            raise TypeError("forecast tool requires ForecastToolInput.")
        return get_forecast(input_data)

    if tool_name == "inventory_status":
        if not isinstance(input_data, InventoryStatusToolInput):
            raise TypeError("inventory_status tool requires InventoryStatusToolInput.")
        return get_inventory_status(input_data)

    if tool_name == "replenishment":
        if not isinstance(input_data, ReplenishmentToolInput):
            raise TypeError("replenishment tool requires ReplenishmentToolInput.")
        return get_replenishment_recommendation_tool(input_data)

    raise ValueError(f"Unsupported tool_name: {tool_name}")