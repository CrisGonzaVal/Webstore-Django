from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
  # Ruta para el admin de Django
    path('admin/', admin.site.urls),

    #conectar mapeo
    # Incluir las URLs de la aplicación 'app
    path('',include('app.urls')),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)