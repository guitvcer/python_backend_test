from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('a/', include('provider_a.urls')),
    path('b/', include('provider_b.urls')),
    path('', include('airflow.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
