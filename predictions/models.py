from django.db import models


class StockPrediction(models.Model):
    stock_name = models.CharField(max_length=50)
    current_price = models.FloatField()
    probability_price_increases = models.FloatField()
    prediction_datetime = models.DateTimeField(auto_now_add=True)  # Change from DateField to DateTimeField

    def __str__(self):
        return (
            f"Buy {self.stock_name} for {self.current_price} with "
            f"{round(self.probability_price_increases * 100, 2)}% "
            f"chance of increase on {self.prediction_datetime}"
        )


class StockData(models.Model):
    stock_name = models.CharField(max_length=50)
    stock_datetime = models.DateTimeField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.BigIntegerField()

    def __str__(self):
        return f"{self.stock_name} on {self.date}: Open={self.open_price}, Close={self.close_price}"
