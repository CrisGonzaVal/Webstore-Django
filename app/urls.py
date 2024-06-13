#se crean los urls de cada vista (html)

from django.urls import path
from .views import (
    home, carro, catalogo, contactanos, login, ofertas, proveedores, registro,
    agregar_producto, eliminar_producto, restar_producto, limpiar_carrito
)

urlpatterns = [
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
]

