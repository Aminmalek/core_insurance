from django.urls import path
from .views import TicketView, ClaimView, DataVendorView,InsuranceConnectoreClaimView

urlpatterns = [
    path('ticket', TicketView.as_view(), name="ticket"),
    path('ticket/<int:id>', TicketView.as_view(), name="ticket"),
    path('claim', ClaimView.as_view(), name="claim"),
    path('claim/<int:id>', ClaimView.as_view(), name="claim"),
    path('claim/name', DataVendorView.as_view(), name="data"),
    path('insurance_connector/claim/<int:id>', InsuranceConnectoreClaimView.as_view(), name="claim"),
]
