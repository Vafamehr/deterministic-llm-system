from typing import List

from sklearn.linear_model import LinearRegression

from .schemas import ForecastFeatureRow
from .features import feature_rows_to_dataframe

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None


def naive_forecast_last_value(rows: List[ForecastFeatureRow]) -> List[float]:
    """
    Naive forecast baseline.

    Prediction rule:
        forecast = lag_1

    This assumes the next demand will equal the most recent observed demand.
    """

    predictions: List[float] = []

    for row in rows:
        pred = row.features.get("lag_1", 0.0)
        predictions.append(pred)

    return predictions


def train_linear_regression_model(feature_df):
    """
    Train a simple linear regression forecasting model.
    """

    X = feature_df.drop(
        columns=["sku_id", "location_id", "date", "target"],
        errors="ignore",
    )
    y = feature_df["target"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def train_xgboost_model(feature_df):
    """
    Train a simple XGBoost regression forecasting model.
    """

    if XGBRegressor is None:
        raise ImportError(
            "xgboost is not installed. Install it with: pip install xgboost"
        )

    X = feature_df.drop(
        columns=["sku_id", "location_id", "date", "target"],
        errors="ignore",
    )
    y = feature_df["target"]

    model = XGBRegressor(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        objective="reg:squarederror",
        random_state=42,
    )
    model.fit(X, y)

    return model


def predict_with_model(model, feature_df):
    """
    Generate predictions using a trained forecasting model.
    """

    X = feature_df.drop(
        columns=["sku_id", "location_id", "date", "prediction_date", "target"],
        errors="ignore",
    )

    predictions = model.predict(X)

    return predictions


def run_linear_regression_training(feature_rows):
    """
    Train a linear regression model from forecasting feature rows
    and return both the model and in-sample predictions.
    """

    feature_df = feature_rows_to_dataframe(feature_rows)

    model = train_linear_regression_model(feature_df)
    predictions = predict_with_model(model, feature_df)

    return model, predictions


def run_xgboost_training(feature_rows):
    """
    Train an XGBoost model from forecasting feature rows
    and return both the model and in-sample predictions.
    """

    feature_df = feature_rows_to_dataframe(feature_rows)

    model = train_xgboost_model(feature_df)
    predictions = predict_with_model(model, feature_df)

    return model, predictions