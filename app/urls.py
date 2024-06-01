from django.urls import path, include
from.views import home
from.views import contacto
from.views import galeria




urlpatterns = [
    path('', home, name="home"),
    path('contacto/', contacto, name="contacto"),
    path('galeria/', galeria, name="galeria"),
]

