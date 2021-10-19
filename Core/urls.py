from django.urls import path
from .views import FileView

urlpatterns = [
    path('media', FileView.as_view(), name="media"),

]
