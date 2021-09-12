from django.urls import path
from .views import InsuranceView

urlpatterns = [
    path('insurance/', InsuranceView.as_view(), name="Insurance"),
]
