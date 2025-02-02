# Generated by Django 5.0.7 on 2024-08-01 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StockData",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("stock_name", models.CharField(max_length=50)),
                ("stock_datetime", models.DateTimeField()),
                ("open_price", models.FloatField()),
                ("high_price", models.FloatField()),
                ("low_price", models.FloatField()),
                ("close_price", models.FloatField()),
                ("volume", models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="StockPrediction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("stock_name", models.CharField(max_length=50)),
                ("predicted_price", models.FloatField()),
                ("prediction_datetime", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
