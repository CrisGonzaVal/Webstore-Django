from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home, carro, catalogo, contactanos, login, ofertas, proveedores, registro, agregar_producto, eliminar_producto, restar_producto, limpiar_carrito, agregar_producto_catalogo
from .views import create_order, capture_order, limpiar_carrito_despues_compra, gracias

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('carro/', carro, name='carro'),
    path('catalogo/', catalogo, name='catalogo'),
    path('contactanos/', contactanos, name='contactanos'),
    path('login/', login, name='login'),
    path('ofertas/', ofertas, name='ofertas'),
    path('proveedores/', proveedores, name='proveedores'),
    path('registro/', registro, name='registro'),
    path('agregar/<int:producto_id>/', agregar_producto, name='agregar_producto'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('restar/<int:producto_id>/', restar_producto, name='restar_producto'),
    path('limpiar/', limpiar_carrito, name='limpiar_carrito'),
    path('agregar_catalogo/<int:producto_id>/', agregar_producto_catalogo, name='agregar_producto_catalogo'),
    path('api/orders', create_order, name='create_order'),
    path('api/orders/<order_id>/capture', capture_order, name='capture_order'),
    path('gracias/', gracias, name='gracias'),
    path('limpiar_carrito_despues_compra/', limpiar_carrito_despues_compra, name='limpiar_carrito_despues_compra'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
