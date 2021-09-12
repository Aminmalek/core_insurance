from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/auth/', include('authenticate.urls')),
    path('api/', include('insured.urls')),
    path('api/', include('insurance.urls')),
]
