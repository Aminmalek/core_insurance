from payment.views import InsuranceConnectorView
from django.urls import path

urlpatterns = [
    path('insurance_connector', InsuranceConnectorView.as_view(), name='insurance_connector'),
    path('insurance_connector/<int:id>', InsuranceConnectorView.as_view(), name='insurance_connector'),
]
