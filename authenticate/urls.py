from django.urls import path
# , DeleteAcountView, GetUsersView
from .views import (SignupView, #CheckAuthenticatedView,
                    LoginView, LogoutView, GetUserView,)


urlpatterns = [
    #path('is_authenticated', CheckAuthenticatedView.as_view(), name="authenticated"),
    path('register', SignupView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('get-user', GetUserView.as_view(), name="get-user"),
    #path('delete', DeleteAcountView.as_view(), name="delete"),
    #path('get_users', GetUsersView.as_view(), name="get_users")
]
