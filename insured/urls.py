from django.urls import path
from .views import InsuredView

urlpatterns = [
    path('insured', InsuredView.as_view(), name="insured"),
    path('insured/<int:id>', InsuredView.as_view(), name="insured"),
]
