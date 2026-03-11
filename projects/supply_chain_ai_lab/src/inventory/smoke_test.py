from .schemas import InventoryRecord
from .service import (
    get_inventory_position,
    get_days_of_supply,
    get_stockout_risk,
)


record = InventoryRecord(
    sku_id="MILK_1L",
    location_id="STORE_102",
    on_hand=120,
    on_order=80,
    reserved=10,
)

inventory_position_result = get_inventory_position(record)
days_of_supply_result = get_days_of_supply(record, expected_daily_demand=20)
stockout_risk_result = get_stockout_risk(
    record,
    expected_daily_demand=20,
    lead_time_days=7,
)

print("Inventory record:")
print(record)

print("\nInventory position result:")
print(inventory_position_result)

print("\nDays of supply result:")
print(days_of_supply_result)

print("\nStockout risk result:")
print(stockout_risk_result)