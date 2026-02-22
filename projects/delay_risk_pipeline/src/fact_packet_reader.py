from __future__ import annotations

import pandas as pd
from pathlib import Path
from typing import List


REQUIRED_COLUMNS = {
    "project_id",
    "weeks_observed",
    "avg_staffing",
    "staffing_volatility",
    "progress",
    "fact_packet",
}


def load_fact_packets(path: str | Path) -> List[str]:
    """
    Load fact packets from CSV and enforce schema contract.

    Returns:
        List[str] → raw fact_packet text blocks
    """
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df["fact_packet"].tolist()


def load_fact_packet_df(path: str | Path) -> pd.DataFrame:
    """
    If later we need structured routing or filtering.
    """
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def get_fact_packets_for_projects(
    df: pd.DataFrame, project_ids: List[str]
) -> List[str]:
    subset = df[df["project_id"].isin(project_ids)]

    if subset.empty:
        raise ValueError("No matching projects found.")

    return subset["fact_packet"].tolist()