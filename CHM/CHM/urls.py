from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('accounts:login')),  # 👈 Root goes to login
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('hospitals/', include('hospitals.urls', namespace='hospitals')),
    path('pharmacy/', include('pharmacy.urls', namespace='pharmacy')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('patients/', include('patients.urls', namespace='patients')),
    path('reports/', include('reports.urls', namespace='reports')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
