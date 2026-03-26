from decision_intelligence.service import classify_decision_intelligence


def run_smoke_tests():
    test_cases = [
        {
            "name": "UNDERSTOCK case",
            "input": {
                "days_of_supply": 0.75,
                "stockout_risk": "HIGH",
                "inventory_pressure": "HIGH",
                "overstock_risk": "LOW",
            },
        },
        {
            "name": "OVERSTOCK case",
            "input": {
                "days_of_supply": 45,
                "stockout_risk": "LOW",
                "inventory_pressure": "LOW",
                "overstock_risk": "HIGH",
            },
        },
        {
            "name": "HIDDEN RISK case",
            "input": {
                "days_of_supply": 7,
                "stockout_risk": "HIGH",
                "inventory_pressure": "MEDIUM",
                "overstock_risk": "LOW",
            },
        },
        {
            "name": "STABLE case",
            "input": {
                "days_of_supply": 12,
                "stockout_risk": "LOW",
                "inventory_pressure": "LOW",
                "overstock_risk": "LOW",
            },
        },
    ]

    print("\n=== V4 DECISION INTELLIGENCE SMOKE TEST ===\n")

    for case in test_cases:
        result = classify_decision_intelligence(**case["input"])

        print(f"Case: {case['name']}")
        print(f"  inventory_state = {result.inventory_state}")
        print(f"  key_risk        = {result.key_risk}")
        print(f"  reasoning       = {result.reasoning_summary}")
        print("-" * 50)


if __name__ == "__main__":
    run_smoke_tests()