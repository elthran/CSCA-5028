import numpy as np
import pandas as pd
from predictions.models import StockData


def sigmoid(z):
    """Compute the sigmoid function"""
    return 1 / (1 + np.exp(-z))


def standardize_data(X):
    """Standardize the features"""
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / std, mean, std


def logistic_regression_fit(X, y, lr=0.01, epochs=1000):
    """Train a logistic regression model using gradient descent"""
    m, n = X.shape
    weights = np.zeros(n)
    bias = 0

    for epoch in range(epochs):
        # Linear combination
        linear_model = np.dot(X, weights) + bias
        # Apply sigmoid function
        y_pred = sigmoid(linear_model)
        # Compute gradients
        dw = (1 / m) * np.dot(X.T, (y_pred - y))
        db = (1 / m) * np.sum(y_pred - y)
        # Update weights and bias
        weights -= lr * dw
        bias -= lr * db

    return weights, bias


def logistic_regression_predict_proba(X, weights, bias):
    """Predict probabilities using logistic regression"""
    linear_model = np.dot(X, weights) + bias
    return sigmoid(linear_model)


def predict_stock():
    # Fetch data from the StockData model
    data = list(StockData.objects.all().values())
    df = pd.DataFrame(data)

    if df.empty:
        df = pd.read_csv("stock_predictions.csv")

    # Preprocess the data
    df = df.sort_values(by="stock_datetime")
    df["price_diff"] = df.groupby("stock_name")["close_price"].diff()
    df["target"] = (df["price_diff"] > 0).astype(int)
    df = df.dropna()

    feature_columns = ["open_price", "high_price", "low_price", "close_price", "volume"]
    models = {}
    scalers = {}

    # Train a logistic regression model for each stock
    for stock_symbol in df["stock_name"].unique():
        stock_df = df[df["stock_name"] == stock_symbol]
        X = stock_df[feature_columns].values
        y = stock_df["target"].values

        # Standardize the features
        X_scaled, mean, std = standardize_data(X)
        scalers[stock_symbol] = (mean, std)

        # Train logistic regression model
        weights, bias = logistic_regression_fit(X_scaled, y)
        models[stock_symbol] = (weights, bias)

    predictions = []

    for stock_symbol in df["stock_name"].unique():
        stock_df = df[df["stock_name"] == stock_symbol]
        latest_data = stock_df[feature_columns].iloc[-1].values.reshape(1, -1)
        mean, std = scalers[stock_symbol]
        latest_data_scaled = (latest_data - mean) / std

        weights, bias = models[stock_symbol]
        prob_increase = logistic_regression_predict_proba(latest_data_scaled, weights, bias)[0]

        random_noise = np.random.normal(0, 0.01)
        prob_increase += random_noise
        prob_increase = np.clip(prob_increase, 0, 1)

        predictions.append((stock_symbol, prob_increase))

    best_stock = max(predictions, key=lambda x: x[1])

    return {
        "best_stock": best_stock[0],
        "probability": best_stock[1]
    }
