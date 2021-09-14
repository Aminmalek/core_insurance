from django.urls import path
from .views import CompanyTicketView, VendorActivatedView

urlpatterns = [
  path('company/tickets', CompanyTicketView.as_view(), name="ticket-company"),
  path('company/vendor-activation', VendorActivatedView.as_view(),name="vendor-avtivation")
]
