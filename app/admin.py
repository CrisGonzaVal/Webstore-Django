from django.contrib import admin

# se registran los modelos (tablas) en el admin

from.models import Categoria, Marca, Producto, Usuario, Cliente, Empleado, Inventario, Dimensiones, Venta, Historial, Fecha, Proveedores, OrdenCompra, Despacho, Direccion, Ciudad, Comuna, TipoPago, ComprobantePago, Cuenta

# Registrar modelos individuales
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto)
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Inventario)
admin.site.register(Dimensiones)
admin.site.register(Venta)
admin.site.register(Historial)
admin.site.register(Fecha)
admin.site.register(Proveedores)
admin.site.register(OrdenCompra)
admin.site.register(Despacho)
admin.site.register(Direccion)
admin.site.register(Ciudad)
admin.site.register(Comuna)
admin.site.register(TipoPago)
admin.site.register(ComprobantePago)
admin.site.register(Cuenta)
