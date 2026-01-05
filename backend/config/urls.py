"""
URL configuration for CryptoMessenger project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/messages/', include('apps.messaging.urls')),
    path('api/crypto/', include('apps.crypto_core.urls')),
    path('api/audit/', include('apps.audit.urls')),
]
