from django.urls import path
from .views import GetGroupView, AddInsuredView, GetRemoveInsuredView


urlpatterns = [

    path('get-user-group', GetGroupView.as_view(), name="getgroup"),
    path('add-new-insured', AddInsuredView.as_view(), name="add-new-insured"),
    path('get-delete-insured', GetRemoveInsuredView.as_view(),
         name="get-delete-insured"),
]
