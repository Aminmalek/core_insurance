from django.urls import path
from .views import InsuranceView

urlpatterns = [
    path('insurance/', InsuranceView.as_view(), name="insurance"),
    path('insurance/<int:id>', InsuranceView.as_view(), name="insurance"),
]
