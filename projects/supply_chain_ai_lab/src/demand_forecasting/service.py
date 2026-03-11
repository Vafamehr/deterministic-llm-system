from .evaluate import evaluate_naive_dataset_with_split


def run_naive_forecast_experiment(dataset, test_size: int):
    """
    Run the baseline naive forecasting experiment
    across the full dataset.
    """

    results = evaluate_naive_dataset_with_split(dataset, test_size)

    return results