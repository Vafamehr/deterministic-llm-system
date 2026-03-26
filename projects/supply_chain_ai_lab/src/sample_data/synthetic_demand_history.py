from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR = Path(__file__).resolve().parent

PRODUCTS_FILE = DATA_DIR / "network_products.csv"
LOCATIONS_FILE = DATA_DIR / "network_locations.csv"


def load_products_table() -> pd.DataFrame:
    """
    Load the product master table.
    """
    return pd.read_csv(PRODUCTS_FILE)


def load_store_locations_table() -> pd.DataFrame:
    """
    Load only store locations from the locations table.
    """
    df = pd.read_csv(LOCATIONS_FILE)
    return df[df["type"] == "store"].copy()


def build_base_demand_table(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
) -> pd.DataFrame:
    """
    Build the full date * sku * store grid that will later
    receive synthetic demand values.
    """
    products_df = load_products_table()
    stores_df = load_store_locations_table()

    dates_df = pd.DataFrame({
        "date": pd.date_range(start=start_date, end=end_date, freq="D")
    })

    products_df = products_df[["sku_id"]].copy()
    stores_df = stores_df[["location_id"]].copy()

    products_df["key"] = 1
    stores_df["key"] = 1
    dates_df["key"] = 1

    base_df = (
        dates_df
        .merge(products_df, on="key")
        .merge(stores_df, on="key")
        .drop(columns="key")
    )

    return base_df






def generate_synthetic_demand_history(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
) -> pd.DataFrame:
    """
    Generate synthetic daily demand for each (sku, store) pair.
    """
    df = build_base_demand_table(start_date, end_date)

    np.random.seed(42)

    # simple base demand by SKU
    base_demand = {
        "sku_1": 35,
        "sku_2": 25,
        "sku_3": 18,
        "sku_4": 10,
    }

    df["base"] = df["sku_id"].map(base_demand)


    noise = np.random.normal(loc=0, scale=5, size=len(df))
    df["units_sold"] = (df["base"] + noise).clip(lower=0).round().astype(int)

    df = df.drop(columns="base")

    return df


def save_synthetic_demand_history(
    output_file: Path = DATA_DIR / "synthetic_demand_history.csv",
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
) -> None:
    """
    Generate the synthetic demand dataset and save it to CSV.
    """
    df = generate_synthetic_demand_history(start_date, end_date)
    df.to_csv(output_file, index=False)

# if __name__ == "__main__":
#     df = generate_synthetic_demand_history()

#     print(df.head())
#     print()
#     print(f"Rows: {len(df)}")

#     save_synthetic_demand_history()
#     print("Synthetic demand history saved.")