from django.urls import path
from . views import TicketByVendorView


urlpatterns = [
    path('tickets/vendor', TicketByVendorView.as_view(), name="ticket-by-vendor")
]
