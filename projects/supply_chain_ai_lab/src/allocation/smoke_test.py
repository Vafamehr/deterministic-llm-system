from allocation.schemas import (
    AllocationRequest,
    LocationDemand,
)
from allocation.service import allocate_inventory


def run_smoke_test():
    allocation_request = AllocationRequest(
        sku_id="sku_1",
        available_inventory=100.0,
        location_demands=[
            LocationDemand(location_id="store_A", demand_units=80.0),
            LocationDemand(location_id="store_B", demand_units=60.0),
            LocationDemand(location_id="store_C", demand_units=50.0),
        ],
    )

    allocation_result = allocate_inventory(allocation_request)

    print("Allocation completed.")
    print(f"SKU: {allocation_result.sku_id}")

    for allocation in allocation_result.allocations:
        print(
            f"{allocation.location_id:<10} allocated_units={allocation.allocated_units:.2f}"
        )


if __name__ == "__main__":
    run_smoke_test()