from django.urls import path
from .views import SuperHolderView

urlpatterns = [
    path('superholder', SuperHolderView.as_view(), name="superholder"),
    path('superholder/<int:id>', SuperHolderView.as_view(), name="superholder")
]
