from pathlib import Path
import pandas as pd


DEMAND_HISTORY_COLUMNS = [
    "date",
    "sku_id",
    "location_id",
    "units_sold",
]


def load_demand_history(csv_path: str | Path) -> pd.DataFrame:
    """
    Load historical demand data for forecasting.

    Expected columns:
    - date
    - sku_id
    - location_id
    - units_sold
    """
    csv_path = Path(csv_path)

    df = pd.read_csv(csv_path)

    missing_columns = [
        column for column in DEMAND_HISTORY_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Demand history file is missing required columns: {missing_columns}"
        )

    df = df[DEMAND_HISTORY_COLUMNS].copy()
    df["date"] = pd.to_datetime(df["date"])
    df["units_sold"] = df["units_sold"].astype(float)

    df = df.sort_values(["sku_id", "location_id", "date"]).reset_index(drop=True)

    return df




