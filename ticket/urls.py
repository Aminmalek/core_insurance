from django.urls import path
from .views import TicketView

urlpatterns = [
  path('ticket', TicketView.as_view(), name="ticket"),
  path('ticket/<int:id>', TicketView.as_view(), name="ticket")
]
