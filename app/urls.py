#se crean los urls de cada vista (html)

from django.urls import path
<<<<<<< HEAD
from.views import home, carro, catalogo, contactanos, login, ofertas, proveedores, registro

=======
from.views import home
from.views import carro
from.views import catalogo
from.views import login
from.views import ofertas
from.views import registro
from.views import agregar_producto, eliminar_producto, restar_producto, limpiar_carrito, agregar_producto_catalogo
>>>>>>> webstore

urlpatterns = [
    path('', home, name='home'),
    path('carro/', carro, name='carro'),
    path('catalogo/', catalogo, name='catalogo'),
    path('login/', login, name='login'),
    path('ofertas/', ofertas, name='ofertas'),
    path('registro/', registro, name='registro'),

    path('agregar/<int:producto_id>/', agregar_producto, name='agregar_producto'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('restar/<int:producto_id>/', restar_producto, name='restar_producto'),
    path('limpiar/', limpiar_carrito, name='limpiar_carrito'),
    path('agregar_catalogo/<int:producto_id>/', agregar_producto_catalogo, name='agregar_producto_catalogo'),
]

