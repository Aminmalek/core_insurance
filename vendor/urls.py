from django.urls import path
from . views import TicketByVendorView


urlpatterns = [
    path('vendor/tickets', TicketByVendorView.as_view(), name="ticket-by-vendor")
]
