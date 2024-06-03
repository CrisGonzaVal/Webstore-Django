from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#se crea la url para el admin django

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings)