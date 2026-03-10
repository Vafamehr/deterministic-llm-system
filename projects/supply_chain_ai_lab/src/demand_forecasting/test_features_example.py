from datetime import date

from .schemas import DemandRecord, DemandDataset
from .features import build_feature_rows_for_dataset, feature_rows_to_dataframe, build_prediction_row_for_series, prediction_row_to_dataframe



def main() -> None:
    dataset = DemandDataset(
        records=[
            # SKU1 - STORE1
            DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 1), demand=10),
            DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 2), demand=12),
            DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 3), demand=14),
            DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 4), demand=16),

            # SKU2 - STORE1
            DemandRecord(sku_id="SKU2", location_id="STORE1", date=date(2024, 1, 1), demand=20),
            DemandRecord(sku_id="SKU2", location_id="STORE1", date=date(2024, 1, 2), demand=22),
            DemandRecord(sku_id="SKU2", location_id="STORE1", date=date(2024, 1, 3), demand=24),
            DemandRecord(sku_id="SKU2", location_id="STORE1", date=date(2024, 1, 4), demand=26),
        ]
    )

    rows = build_feature_rows_for_dataset(
        dataset=dataset,
        lag_steps=[1, 2],
        rolling_windows=[3],
    )


    df = feature_rows_to_dataframe(rows)

    print("\nFeature table:\n")
    print(df)

    assert len(rows) == 2

    row_1 = next(r for r in rows if r.sku_id == "SKU1" and r.location_id == "STORE1")
    assert row_1.date == date(2024, 1, 4)
    assert row_1.features["lag_1"] == 14.0
    assert row_1.features["lag_2"] == 12.0
    assert row_1.features["rolling_mean_3"] == 12.0
    assert row_1.target == 16.0

    row_2 = next(r for r in rows if r.sku_id == "SKU2" and r.location_id == "STORE1")
    assert row_2.date == date(2024, 1, 4)
    assert row_2.features["lag_1"] == 24.0
    assert row_2.features["lag_2"] == 22.0
    assert row_2.features["rolling_mean_3"] == 22.0
    assert row_2.target == 26.0

    print("Full dataset feature pipeline test passed.")


    prediction_row = build_prediction_row_for_series(
    series=[
        DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 1), demand=10),
        DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 2), demand=12),
        DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 3), demand=14),
        DemandRecord(sku_id="SKU1", location_id="STORE1", date=date(2024, 1, 4), demand=16),
    ],
    lag_steps=[1, 2],
    rolling_windows=[3],
    )

    print("\nPrediction row:\n")
    print(prediction_row)

    assert prediction_row.sku_id == "SKU1"
    assert prediction_row.location_id == "STORE1"
    assert prediction_row.prediction_date == date(2024, 1, 5)
    assert prediction_row.features["lag_1"] == 16.0
    assert prediction_row.features["lag_2"] == 14.0
    assert prediction_row.features["rolling_mean_3"] == 14.0

    prediction_df = prediction_row_to_dataframe(prediction_row)

    print("\nPrediction feature table:\n")
    print(prediction_df)


if __name__ == "__main__":
    main()