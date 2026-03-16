from __future__ import annotations

from network_monitoring.schemas import (
    NetworkHealthReport,
    NetworkInventoryRecord,
    StockoutRisk,
)


def build_network_health_report(
    inventory_records: list[NetworkInventoryRecord],
    days_of_supply_threshold: float = 3.0,
) -> NetworkHealthReport:
    stockout_risks: list[StockoutRisk] = []

    for record in inventory_records:
        if record.expected_daily_demand <= 0:
            continue

        days_of_supply = record.on_hand / record.expected_daily_demand

        if days_of_supply <= days_of_supply_threshold:
            stockout_risks.append(
                StockoutRisk(
                    sku_id=record.sku_id,
                    location_id=record.location_id,
                    days_of_supply=days_of_supply,
                )
            )

    return NetworkHealthReport(stockout_risks=stockout_risks)