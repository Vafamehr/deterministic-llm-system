from network_monitoring.schemas import NetworkInventoryRecord
from network_monitoring.service import build_network_health_report


def run_smoke_test():
    inventory_records = [
        NetworkInventoryRecord(
            sku_id="sku_1",
            location_id="store_A",
            on_hand=100.0,
            expected_daily_demand=20.0,
        ),
        NetworkInventoryRecord(
            sku_id="sku_1",
            location_id="store_B",
            on_hand=30.0,
            expected_daily_demand=15.0,
        ),
        NetworkInventoryRecord(
            sku_id="sku_1",
            location_id="store_C",
            on_hand=10.0,
            expected_daily_demand=12.0,
        ),
    ]

    report = build_network_health_report(inventory_records)

    print("Network Health Report")
    print("---------------------")

    for risk in report.stockout_risks:
        print(
            f"{risk.location_id:<10} {risk.sku_id:<10} days_of_supply={risk.days_of_supply:.2f}"
        )


if __name__ == "__main__":
    run_smoke_test()