from disruption_modeling.schemas import (
    DisruptionType,
    SeverityLevel,
    AffectedNode,
    DisruptionEvent,
    DisruptionImpact,
    DisruptionScenario,
)

from disruption_modeling.service import resolve_disruption


def run_smoke_test():
    affected_node = AffectedNode(
        node_id="supplier_A",
        node_type="supplier",
    )

    event = DisruptionEvent(
        event_id="event_1",
        disruption_type=DisruptionType.SUPPLIER_DELAY,
        severity=SeverityLevel.HIGH,
        duration_days=5,
        affected_node=affected_node,
        description="Supplier shipment delay",
    )

    impact = DisruptionImpact(
        supplier_delay_days=5,
    )

    scenario = DisruptionScenario(
        scenario_name="supplier_delay_test",
        event=event,
        impact=impact,
    )

    resolved = resolve_disruption(scenario)

    print("Disruption resolved:")
    print(resolved)


if __name__ == "__main__":
    run_smoke_test()