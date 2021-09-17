from django.urls import path
from .views import TicketView

urlpatterns = [
  path('insured/tickets', TicketView.as_view(), name="ticket")
]
