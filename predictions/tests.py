from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import StockPrediction


class StockPredictionModelTest(TestCase):

    def test_create_stock_prediction(self):
        # Create a new stock prediction
        stock_name = "AAPL"
        predicted_price = 150.00
        prediction_datetime = timezone.now()
        prediction = StockPrediction.objects.create(
            stock_name=stock_name, predicted_price=predicted_price, prediction_datetime=prediction_datetime
        )

        # Retrieve the prediction from the database
        saved_prediction = StockPrediction.objects.get(id=prediction.id)

        # Check if the saved prediction matches the created one (up to the second)
        self.assertEqual(saved_prediction.stock_name, stock_name)
        self.assertEqual(saved_prediction.predicted_price, predicted_price)
        self.assertEqual(
            saved_prediction.prediction_datetime.replace(microsecond=0), prediction_datetime.replace(microsecond=0)
        )


class StockPredictionIntegrationTest(TestCase):

    def test_homepage_displays_latest_prediction(self):
        # Create a stock prediction
        stock_name = "AAPL"
        predicted_price = 150.00
        StockPrediction.objects.create(stock_name=stock_name, predicted_price=predicted_price)

        # Get the homepage
        response = self.client.get(reverse("index"))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the latest prediction is in the context
        self.assertContains(response, stock_name)
        self.assertContains(response, predicted_price)

    def test_refresh_prediction_button(self):
        # Post to the fetch_data URL to create a new prediction
        response = self.client.post(reverse("fetch_data"))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that a new prediction was created
        self.assertEqual(StockPrediction.objects.count(), 1)

        # Check that the new prediction is displayed on the homepage
        latest_prediction = StockPrediction.objects.latest("prediction_datetime")
        response = self.client.get(reverse("index"))
        self.assertContains(response, latest_prediction.stock_name)
        self.assertContains(response, latest_prediction.predicted_price)
