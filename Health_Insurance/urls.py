from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/auth/', include('authenticate.urls')),
    path('api/', include('insured.urls')),
    path('api/', include('insurance.urls')),
    path('api/', include('ticket.urls')),
    path('api/', include('payment.urls')),
    path('api/', include('vendor.urls')),
    path('api/', include('company.urls')),
    path('api/', include('super_holder.urls')),
]
