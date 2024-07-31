# predictions/views.py

from django.shortcuts import render
from .models import StockPrediction
import requests
from django.views.decorators.csrf import csrf_exempt


def index(request):
    # Fetch the latest prediction from the database
    latest_prediction = StockPrediction.objects.order_by("-prediction_date").first()
    context = {"latest_prediction": latest_prediction}
    return render(request, "index.html", context)


@csrf_exempt  # Disable CSRF for simplicity, but not recommended for production
def fetch_data(request):
    if request.method == "POST":
        # Replace with actual API call
        stock_name = "AAPL"
        api_url = "https://api.example.com/stock_data"
        response = requests.get(api_url, params={"stock": stock_name})

        if response.status_code == 200:
            data = response.json()
            predicted_price = data.get("predicted_price", 150.00)  # Replace with actual data extraction
        else:
            stock_name = "Error"
            predicted_price = 0.00

        # Save the prediction to the database
        prediction = StockPrediction(stock_name=stock_name, predicted_price=predicted_price)
        prediction.save()

        latest_prediction = StockPrediction.objects.order_by("-prediction_date").first()
        context = {"latest_prediction": latest_prediction}
        return render(request, "index.html", context)
    else:
        return render(request, "index.html")


def previous_predictions(request):
    # Fetch all previous predictions from the database
    predictions = StockPrediction.objects.all().order_by("-prediction_date")
    context = {"predictions": predictions}
    return render(request, "previous_predictions.html", context)
