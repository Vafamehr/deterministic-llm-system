from __future__ import annotations

from allocation.schemas import (
    AllocationRequest,
    AllocationResult,
    LocationAllocation,
)


def allocate_inventory(allocation_request: AllocationRequest) -> AllocationResult:
    total_demand = sum(
        location_demand.demand_units
        for location_demand in allocation_request.location_demands
    )

    if total_demand <= 0:
        return AllocationResult(
            sku_id=allocation_request.sku_id,
            allocations=[
                LocationAllocation(
                    location_id=location_demand.location_id,
                    allocated_units=0.0,
                )
                for location_demand in allocation_request.location_demands
            ],
        )

    if allocation_request.available_inventory >= total_demand:
        return AllocationResult(
            sku_id=allocation_request.sku_id,
            allocations=[
                LocationAllocation(
                    location_id=location_demand.location_id,
                    allocated_units=location_demand.demand_units,
                )
                for location_demand in allocation_request.location_demands
            ],
        )

    allocation_ratio = allocation_request.available_inventory / total_demand

    allocations = [
        LocationAllocation(
            location_id=location_demand.location_id,
            allocated_units=location_demand.demand_units * allocation_ratio,
        )
        for location_demand in allocation_request.location_demands
    ]

    return AllocationResult(
        sku_id=allocation_request.sku_id,
        allocations=allocations,
    )