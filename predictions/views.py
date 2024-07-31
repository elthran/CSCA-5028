from django.shortcuts import render
from .models import StockPrediction
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import random


def index(request):
    # Fetch the latest prediction from the database
    latest_prediction = StockPrediction.objects.order_by("-prediction_datetime").first()
    time_since_last_prediction = None
    days = hours = minutes = 0
    if latest_prediction:
        time_since_last_prediction = timezone.now() - latest_prediction.prediction_datetime
        days = time_since_last_prediction.days
        hours = time_since_last_prediction.seconds // 3600
        minutes = (time_since_last_prediction.seconds // 60) % 60

    context = {
        "latest_prediction": latest_prediction,
        "days": days,
        "hours": hours,
        "minutes": minutes,
    }
    return render(request, "index.html", context)


@csrf_exempt  # Disable CSRF for simplicity, but not recommended for production
def fetch_data(request):
    if request.method == "POST":
        # Generate random stock name and price
        stock_names = ["AAPL", "GOOGL", "MSFT", "AMZN", "FB"]
        stock_name = random.choice(stock_names)
        predicted_price = round(random.uniform(100, 1500), 2)

        # Save the prediction to the database
        prediction = StockPrediction(
            stock_name=stock_name, predicted_price=predicted_price, prediction_datetime=timezone.now()
        )
        prediction.save()

    # After saving the new prediction, redirect to the home page
    return index(request)


def previous_predictions(request):
    # Fetch all previous predictions from the database
    predictions = StockPrediction.objects.all().order_by("-prediction_datetime")
    context = {"predictions": predictions}
    return render(request, "previous_predictions.html", context)
