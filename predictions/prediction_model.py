import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from predictions.models import StockData


def predict_stock():
    # Fetch data from the StockData model
    data = list(StockData.objects.all().values())
    df = pd.DataFrame(data)

    if df.empty:
        df = pd.read_csv("stock_predictions.csv")

    # Step 2: Preprocess the data
    # Sort by datetime to ensure time series order
    df = df.sort_values(by="stock_datetime")

    # Create new feature columns
    df["price_diff"] = df.groupby("stock_name")["close_price"].diff()  # Price difference between consecutive days
    df["target"] = (df["price_diff"] > 0).astype(int)  # Target: 1 if price increased, 0 otherwise

    # Drop rows with NaN values created by the diff() function
    df = df.dropna()

    # Define feature columns
    feature_columns = ["open_price", "high_price", "low_price", "close_price", "volume"]

    # Initialize a dictionary to store models and scalers for each stock
    models = {}
    scalers = {}

    # Step 3: Train a logistic regression model for each stock
    for stock_symbol in df["stock_name"].unique():
        stock_df = df[df["stock_name"] == stock_symbol]

        # Split data into features and target
        X = stock_df[feature_columns]
        y = stock_df["target"]

        # Standardize the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train the logistic regression model
        model = LogisticRegression()
        model.fit(X_scaled, y)

        # Store the model and scaler for this stock
        models[stock_symbol] = model
        scalers[stock_symbol] = scaler

    # Step 4: Predict for the next day using the latest available data for each stock
    predictions = []

    for stock_symbol in df["stock_name"].unique():
        stock_df = df[df["stock_name"] == stock_symbol]

        # Get the latest row of features
        latest_data = stock_df[feature_columns].iloc[-1].to_frame().T

        # Standardize the latest data using the corresponding scaler
        latest_data_scaled = scalers[stock_symbol].transform(latest_data)

        # Predict the probability of the stock price increasing
        prob_increase = models[stock_symbol].predict_proba(latest_data_scaled)[0][1]

        # Add randomness to the probability
        random_noise = np.random.normal(0, 0.01)  # Small Gaussian noise
        prob_increase += random_noise
        prob_increase = np.clip(prob_increase, 0, 1)  # Ensure the probability stays between 0 and 1

        # Append the stock symbol and its probability to the predictions list
        predictions.append((stock_symbol, prob_increase))

    # Step 5: Identify the stock with the highest probability of increasing
    best_stock = max(predictions, key=lambda x: x[1])

    return {"best_stock": best_stock[0], "probability": best_stock[1]}
