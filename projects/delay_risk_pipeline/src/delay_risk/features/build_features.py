"""
Feature construction layer.

This converts validated rows into structured signals.
No file access. No validation. Just transformations.
"""

import pandas as pd


import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # 1) history length per project
    out["weeks_observed"] = (
        out.groupby("project_id")["snapshot_week"]
        .transform("count")
    )

    # 2) lifecycle progress (0-1 within each project)
    max_week = out.groupby("project_id")["snapshot_week"].transform("max")
    out["week_progress"] = out["snapshot_week"] / max_week

    # 3) change signal (instability proxy)
    if "staffing_level" in out.columns:
        out["staffing_delta"] = (
            out.groupby("project_id")["staffing_level"]
            .diff()
            .fillna(0)
        )

    # 4) rolling variability (more instability)
    if "staffing_level" in out.columns:
        out["staffing_roll_std_3"] = (
            out.groupby("project_id")["staffing_level"]
            .rolling(window=3, min_periods=2)
            .std()
            .reset_index(level=0, drop=True)
            .fillna(0)
        )

    return out

