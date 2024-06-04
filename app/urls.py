#se crean los urls de cada vista (html)

from django.urls import path
from.views import home
from.views import carro
from.views import catalogo
from.views import contactanos
from.views import login
from.views import ofertas
from.views import proveedores
from.views import registro

urlpatterns = [
    path('', home, name='home'),
    path('carro/', carro, name='carro'),
    path('catalogo/', catalogo, name='catalogo'),
    path('contactanos/', contactanos, name='contactanos'),
    path('login/', login, name='login'),
    path('ofertas/', ofertas, name='ofertas'),
    path('proveedores/', proveedores, name='proveedores'),
    path('registro/', registro, name='registro'),
]

