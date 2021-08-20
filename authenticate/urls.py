from django.urls import path
from .views import (SignupView,LoginView, LogoutView, GetUserView,)


urlpatterns = [

    path('register', SignupView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('get-user', GetUserView.as_view(), name="get-user"),
]
