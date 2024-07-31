from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("predict/", views.predict_stock, name="predict_stock"),
    path("previous_predictions/", views.previous_predictions, name="previous_predictions"),
]
