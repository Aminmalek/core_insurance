from django.urls import path
from .views import TicketView, ClaimView

urlpatterns = [
    path('ticket', TicketView.as_view(), name="ticket"),
    path('ticket/<int:id>', TicketView.as_view(), name="ticket"),
    path('claim/', ClaimView.as_view(), name="claim"),
    path('claim/<int:id>', ClaimView.as_view(), name="claim"),
]
