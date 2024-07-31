from django.db import models


class StockPrediction(models.Model):
    stock_name = models.CharField(max_length=50)
    predicted_price = models.FloatField()
    prediction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_name} - {self.predicted_price}"
