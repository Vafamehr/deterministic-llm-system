import pandas as pd
from delay_risk.features.build_features import build_features

df = pd.DataFrame(
    {
        "project_id": ["A", "A", "A", "B", "B"],
        "snapshot_week": [1, 2, 3, 1, 2],
        "staffing_level": [10, 9, 11, 5, 7],
    }
)

print(build_features(df))
