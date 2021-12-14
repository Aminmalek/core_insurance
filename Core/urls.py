from django.urls import path,include
from .views import FileView, MessageViewSet
from rest_framework.routers import DefaultRouter,SimpleRouter

router = SimpleRouter()
router.register('message', MessageViewSet, basename='message')


urlpatterns = [
    path('media', FileView.as_view(), name="media"),
    path('', include(router.urls)),
   
]
