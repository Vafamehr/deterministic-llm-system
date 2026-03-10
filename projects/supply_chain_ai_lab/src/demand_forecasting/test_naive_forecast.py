from datetime import date
import pytest

from .schemas import DemandRecord, DemandDataset
from .evaluate import (
    evaluate_naive_on_series,
    evaluate_naive_on_dataset,
    mean_mae_across_series,
)


def test_evaluate_naive_on_series():
    """
    Test naive forecast evaluation on a simple demand series.
    """
    series = [
        DemandRecord("SKU1", "LOC1", date(2025, 1, 1), 10.0),
        DemandRecord("SKU1", "LOC1", date(2025, 1, 2), 12.0),
        DemandRecord("SKU1", "LOC1", date(2025, 1, 3), 11.0),
        DemandRecord("SKU1", "LOC1", date(2025, 1, 4), 15.0),
    ]

    result = evaluate_naive_on_series(series)

    assert result == 2.3333333333333335


def test_evaluate_naive_on_series_raises_for_short_series():
    """
    A series with fewer than two observations cannot be evaluated.
    """
    series = [
        DemandRecord("SKU1", "LOC1", date(2025, 1, 1), 10.0),
    ]

    with pytest.raises(ValueError, match="Series must contain at least two observations"):
        evaluate_naive_on_series(series)


def test_evaluate_naive_on_dataset():
    dataset = DemandDataset(
        records=[
            DemandRecord("SKU1", "LOC1", date(2025, 1, 1), 10.0),
            DemandRecord("SKU1", "LOC1", date(2025, 1, 2), 12.0),
            DemandRecord("SKU1", "LOC1", date(2025, 1, 3), 11.0),
            DemandRecord("SKU1", "LOC1", date(2025, 1, 4), 15.0),
            DemandRecord("SKU2", "LOC2", date(2025, 1, 1), 20.0),
            DemandRecord("SKU2", "LOC2", date(2025, 1, 2), 18.0),
            DemandRecord("SKU2", "LOC2", date(2025, 1, 3), 21.0),
        ]
    )

    result = evaluate_naive_on_dataset(dataset)

    assert result == {
        ("SKU1", "LOC1"): 2.3333333333333335,
        ("SKU2", "LOC2"): 2.5,
    }


def test_evaluate_naive_on_dataset_skips_short_series():
    dataset = DemandDataset(
        records=[
            DemandRecord("SKU1", "LOC1", date(2025, 1, 1), 10.0),
            DemandRecord("SKU1", "LOC1", date(2025, 1, 2), 12.0),
            DemandRecord("SKU2", "LOC2", date(2025, 1, 1), 20.0),
        ]
    )

    result = evaluate_naive_on_dataset(dataset)

    assert result == {
        ("SKU1", "LOC1"): 2.0,
    }


def test_mean_mae_across_series():
    results = {
        ("SKU1", "LOC1"): 2.3333333333333335,
        ("SKU2", "LOC2"): 2.5,
    }

    result = mean_mae_across_series(results)

    assert result == 2.416666666666667





def test_mean_mae_across_series_raises_for_empty_results():
    with pytest.raises(ValueError, match="results cannot be empty"):
        mean_mae_across_series({})