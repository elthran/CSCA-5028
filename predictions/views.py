from django.shortcuts import render
from .models import StockPrediction
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


@csrf_exempt  # Disable CSRF for simplicity, but not recommended for production
def predict_stock(request):
    if request.method == "POST":
        # Logic for predicting stock (replace with actual prediction code)
        stock_name = "AAPL"
        predicted_price = 150.00

        # Save prediction to database (optional)
        prediction = StockPrediction(stock_name=stock_name, predicted_price=predicted_price)
        prediction.save()

        context = {"stock_name": stock_name, "predicted_price": predicted_price}
        return render(request, "result.html", context)
    else:
        return render(request, "index.html")


def previous_predictions(request):
    predictions = StockPrediction.objects.all()
    return render(request, "previous_predictions.html", {"predictions": predictions})
