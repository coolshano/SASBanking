from django.urls import path
from .views import fraud_dashboard

urlpatterns = [
    path("dashboard/", fraud_dashboard, name="fraud_dashboard"),
]