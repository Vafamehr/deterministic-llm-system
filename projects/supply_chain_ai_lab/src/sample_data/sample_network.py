import pandas as pd

from inventory.schemas import InventoryRecord
from sample_data.schemas import (
    LocationRecord,
    ProductRecord,
    SupplierRecord,
    TransportationLaneRecord,
)

from sample_data.schemas import SampleNetwork

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent


def load_inventory_snapshot() -> list[InventoryRecord]:
    """
    Load the current inventory snapshot from CSV
    and convert each row into an InventoryRecord.
    """
  
    df = pd.read_csv(DATA_DIR /"inventory_snapshot.csv")
    rows = df.to_dict(orient="records")
    return [InventoryRecord(**row) for row in rows]


def load_products() -> list[ProductRecord]:
    """
    Load product data from CSV and convert rows to ProductRecord objects.
    """
    df = pd.read_csv(DATA_DIR /"network_products.csv")
    
    rows = df.to_dict(orient="records")
    return [ProductRecord(**row) for row in rows]


def load_locations() -> list[LocationRecord]:
    """
    Load location data from CSV and convert rows to LocationRecord objects.
    """
    df = pd.read_csv(DATA_DIR /"network_locations.csv")
    rows = df.to_dict(orient="records")
    return [LocationRecord(**row) for row in rows]


def load_suppliers() -> list[SupplierRecord]:
    """
    Load supplier data from CSV and convert rows to SupplierRecord objects.
    """

    df = pd.read_csv(DATA_DIR /"network_suppliers.csv")
    rows = df.to_dict(orient="records")
    return [SupplierRecord(**row) for row in rows]


def load_transportation_lanes() -> list[TransportationLaneRecord]:
    """
    Load transportation lane data from CSV
    and convert rows to TransportationLaneRecord objects.
    """
 
    df = pd.read_csv(DATA_DIR /"network_lanes.csv")
    
    rows = df.to_dict(orient="records")
    return [TransportationLaneRecord(**row) for row in rows]



def build_sample_network() -> SampleNetwork:
    """
    Build the full sample supply chain network by loading
    all network datasets.
    """
    products = load_products()
    locations = load_locations()
    suppliers = load_suppliers()
    lanes = load_transportation_lanes()
    inventory = load_inventory_snapshot()

    return SampleNetwork(
        products=products,
        locations=locations,
        suppliers=suppliers,
        lanes=lanes,
        inventory=inventory,
    )



if __name__ == "__main__":
    network = build_sample_network()
    df_inventory = pd.DataFrame(r for r in network.inventory)


    # print("Products:", len(network.products))
    # print("Locations:", len(network.locations))
    # print("Suppliers:", len(network.suppliers))
    # print("Lanes:", len(network.lanes))
    # print("Inventory records:", len(network.inventory))
    # print(network.inventory)
    # df2= pd.DataFrame([r for r in network.inventory])
    # print(df2)