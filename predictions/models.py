from django.db import models


class StockPrediction(models.Model):
    stock_name = models.CharField(max_length=50)
    predicted_price = models.FloatField()
    prediction_datetime = models.DateTimeField(auto_now_add=True)  # Change from DateField to DateTimeField

    def __str__(self):
        return f"{self.stock_name} - {self.predicted_price} on {self.prediction_datetime}"
