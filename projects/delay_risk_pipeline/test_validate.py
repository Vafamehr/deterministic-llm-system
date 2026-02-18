# import pandas as pd
# from delay_risk.validation.validate import validate_inputs

# # Intentionally broken: duplicate key
# df = pd.DataFrame(
#     {
#         "project_id": ["A", "A"],
#         "snapshot_week": [1, 1],
#         "will_slip_4_6w": [True, False],
#     }
# )

# res = validate_inputs(df, mode="train")

# print("OK:", res.ok)
# print("Errors:")
# for e in res.errors:
#     print("-", e)
# print("Stats:", res.stats)


import pandas as pd

from delay_risk.validation.validate import ValidationRules, validate_inputs
from delay_risk.validation.validate import write_validation_report


rules = ValidationRules(
    max_missing_frac=0.5,
    numeric_ranges={"risk_score": (0.0, 1.0), "weather_risk_score": (0.0, 1.0)},
)



# Intentionally messy dataframe to trigger warnings/errors
df = pd.DataFrame(
    {
        "project_id": ["A", "A", "B", "C"],
        "snapshot_week": [1, 1, 2, 3],  # duplicate for A
        "will_slip_4_6w": [True, False, True, True],

        # 75% missing → should trigger missingness warning
        "weather_risk_score": [None, None, None, 0.3],

        # invalid range → should trigger error
        "risk_score": [0.2, 1.2, 0.5, -0.1],
    }
)

res = validate_inputs(df, mode="train", rules=rules)

print("OK:", res.ok)

print("\nErrors:")
for e in res.errors:
    print("-", e)

print("\nWarnings:")
for w in res.warnings:
    print("-", w)

print("\nStats:", res.stats)


report_path = write_validation_report(
    res,
    output_dir="outputs",
    mode="train"
)

print("Validation report written to:", report_path)

