# predictions/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("fetch_data/", views.fetch_data, name="fetch_data"),
    path("previous_predictions/", views.previous_predictions, name="previous_predictions"),
]
