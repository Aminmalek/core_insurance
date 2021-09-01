from django.urls import path
from .views import GetGroupView


urlpatterns = [

    path('get-user-group', GetGroupView.as_view(), name="getgroup"),
]
