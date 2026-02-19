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


def load_fact_packets(path: str | Path) -> pd.DataFrame:
    """
    Load fact packets from CSV and enforce schema contract.
    """
    df = pd.read_csv(path)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df


def get_fact_packets_for_projects(
    df: pd.DataFrame, project_ids: List[str]
) -> List[str]:
    """
    Retrieve fact_packet text blocks for selected projects.
    """
    subset = df[df["project_id"].isin(project_ids)]

    if subset.empty:
        raise ValueError("No matching projects found.")

    return subset["fact_packet"].tolist()
