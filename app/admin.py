from django.contrib import admin

# se registran los modelos (tablas) en el admin

from.models import Marca, Producto

admin.site.register(Marca)
admin.site.register(Producto)
