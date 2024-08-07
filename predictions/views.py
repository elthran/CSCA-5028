from datetime import datetime

import pytz
import requests
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import StockPrediction, StockData
from .prediction_model import predict_stock

alpha_vantage_api_key = "0DNCB07LVBWZTK6M"
alpha_vantage_endpoint = "https://www.alphavantage.co/query"


def fetch_stock_data(symbol):
    """
    Fetch stock price data for a given symbol and date range from Alpha Vantage API.

    Parameters:
    symbol (str): The stock ticker symbol (e.g., 'AAPL' for Apple).
    start_date (str): The start date for fetching data in 'YYYY-MM-DD' format.
    end_date (str): The end date for fetching data in 'YYYY-MM-DD' format.

    Returns:
    list: A list of dictionaries containing the stock price data.
    """
    # Parameters to be sent in the GET request
    params = {
        "function": "TIME_SERIES_INTRADAY",  # Function to fetch intraday time series
        "symbol": symbol,
        "apikey": alpha_vantage_api_key,
        "outputsize": "full",  # Retrieve the full-length time series
        "datatype": "json",
        "interval": "60min",
    }

    try:
        # Sending a GET request to the API endpoint with the parameters
        response = requests.get(alpha_vantage_endpoint, params=params)

        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract time series data
            time_series = data.get("Time Series (60min)", {})

            if time_series == {}:
                return "Failure"

            for datetime_str, values in time_series.items():

                # Convert datetime string to date object
                datetime_obj = pytz.utc.localize(datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S"))

                try:
                    StockData.objects.update_or_create(
                        stock_name=symbol,
                        stock_datetime=datetime_obj,
                        defaults={
                            "open_price": float(values["1. open"]),
                            "high_price": float(values["2. high"]),
                            "low_price": float(values["3. low"]),
                            "close_price": float(values["4. close"]),
                            "volume": int(values["5. volume"]),
                        },
                    )
                except Exception as e:
                    print(f"Error saving data for {symbol} at {datetime_obj}: {e}")
        else:
            # Print an error message if the response status code is not 200
            print(f"Error: {response.status_code}")
            print(response.json())
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"Request failed: {e}")


def index(request):
    latest_prediction = StockPrediction.objects.order_by("-prediction_datetime").first()
    days = hours = minutes = 0

    if latest_prediction:
        time_since_last_prediction = timezone.now() - latest_prediction.prediction_datetime
        days = time_since_last_prediction.days
        hours = time_since_last_prediction.seconds // 3600
        minutes = (time_since_last_prediction.seconds // 60) % 60
        latest_prediction.probability_price_increases *= 100

    context = {
        "latest_prediction": latest_prediction,
        "days": days,
        "hours": hours,
        "minutes": minutes,
    }
    return render(request, "index.html", context)


@csrf_exempt
def fetch_data(request):
    if request.method == "POST":
        stock_names = [
            "NVDA",
            "AMD",
            "LUMN",
            "F",
            "TSLA",
            "SOFI",
            "ABEV",
            "PLUG",
            "AVGO",
            "INTC",
            "MSFT",
            "KVUE",
            "BAC",
            "PINS",
            "AAL",
            "AAPL",
            "CCL",
            "NIO",
            "BBD",
            "VALE",
            "AMZN",
            "LCID",
            "PFE",
            "TEVA",
            "MARA",
        ]

        current_day = timezone.now().date()

        latest_stock_data = StockData.objects.order_by("-stock_datetime").first()
        fetch_new_data = not latest_stock_data or latest_stock_data.stock_datetime.date() != current_day

        if fetch_new_data:  # Iterate over all stocks and fetch up to date data
            for stock_name in stock_names:
                results = fetch_stock_data(stock_name)

                if results == "Failure":
                    break

        # Predict the best stock to buy based on historical trends using Logistic Regression
        prediction = predict_stock()

        stock = StockData.objects.filter(stock_name=prediction["best_stock"]).order_by("-stock_datetime").first()

        prediction = StockPrediction(
            stock_name=stock.stock_name,
            current_price=stock.close_price,
            probability_price_increases=prediction["probability"],
            prediction_datetime=timezone.now(),
        )
        prediction.save()

        context = {
            "stock_name": prediction.stock_name,
            "current_price": prediction.current_price,
            "probability_price_increases": round(prediction.probability_price_increases * 100, 2),
            "prediction_datetime": prediction.prediction_datetime,
        }
        return render(request, "result.html", context)

    return index(request)


def previous_predictions(request):
    # Fetch all previous predictions from the database
    predictions = StockPrediction.objects.all().order_by("-prediction_datetime")
    for prediction in predictions:
        prediction.probability_price_increases = round(prediction.probability_price_increases * 100, 2)
    context = {"predictions": predictions}
    return render(request, "previous_predictions.html", context)
