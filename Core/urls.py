from django.urls import path
from .views import FileView,MessageView

urlpatterns = [
    path('media', FileView.as_view(), name="media"),
    path('message', MessageView.as_view(), name="message"),
    path('message/<int:id>', MessageView.as_view(), name="message"),
]
