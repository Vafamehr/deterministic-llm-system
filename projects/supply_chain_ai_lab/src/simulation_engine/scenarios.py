from simulation_engine.schemas import Scenario


def build_baseline_scenario() -> Scenario:
    """
    Baseline scenario with no changes applied.
    """
    return Scenario(
        name="baseline",
        description="No disruption applied. Uses the original baseline input.",
        demand_multiplier=1.0,
        lead_time_multiplier=1.0,
        inventory_multiplier=1.0,
    )


def build_demand_spike_scenario(multiplier: float = 1.3) -> Scenario:
    """
    Simulates a sudden increase in demand.
    """
    return Scenario(
        name="demand_spike",
        description="Demand increases above normal baseline levels.",
        demand_multiplier=multiplier,
        lead_time_multiplier=1.0,
        inventory_multiplier=1.0,
        metadata={"scenario_type": "demand"},
    )


def build_supplier_delay_scenario(multiplier: float = 1.5) -> Scenario:
    """
    Simulates slower replenishment due to supplier or transit delay.
    """
    return Scenario(
        name="supplier_delay",
        description="Lead times increase due to supplier or logistics disruption.",
        demand_multiplier=1.0,
        lead_time_multiplier=multiplier,
        inventory_multiplier=1.0,
        metadata={"scenario_type": "supply"},
    )


def build_inventory_shock_scenario(multiplier: float = 0.7) -> Scenario:
    """
    Simulates a sudden drop in available inventory.
    """
    return Scenario(
        name="inventory_shock",
        description="Available inventory drops below the normal baseline.",
        demand_multiplier=1.0,
        lead_time_multiplier=1.0,
        inventory_multiplier=multiplier,
        metadata={"scenario_type": "inventory"},
    )


def build_promotion_event_scenario(multiplier: float = 1.5) -> Scenario:
    """
    Simulates a promotion-driven demand uplift.
    """
    return Scenario(
        name="promotion_event",
        description="Promotional activity causes a temporary demand increase.",
        demand_multiplier=multiplier,
        lead_time_multiplier=1.0,
        inventory_multiplier=1.0,
        metadata={"scenario_type": "promotion"},
    )