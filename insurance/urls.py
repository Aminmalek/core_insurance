from django.urls import path
from .views import InsuranceAddView

urlpatterns = [

    path('add-new-insurance/', InsuranceAddView.as_view(), name="AddNewInsurance"),
]
