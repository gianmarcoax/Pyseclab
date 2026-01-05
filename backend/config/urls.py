"""
URL configuration for PySec Lab project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import FileResponse
import os

# Vista para servir el frontend React
def serve_frontend(request):
    """Sirve el index.html del frontend React"""
    frontend_path = os.path.join(settings.BASE_DIR.parent, 'frontend', 'dist', 'index.html')
    if os.path.exists(frontend_path):
        return FileResponse(open(frontend_path, 'rb'), content_type='text/html')
    else:
        from django.http import HttpResponse
        return HttpResponse("Frontend no encontrado. Ejecuta 'npm run build' en la carpeta frontend.", status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/messages/', include('apps.messaging.urls')),
    path('api/crypto/', include('apps.crypto_core.urls')),
    path('api/audit/', include('apps.audit.urls')),
]

# En producción, servir el frontend React
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^(?!api|admin|static).*$', serve_frontend),
    ]
