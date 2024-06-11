from django.contrib import admin

# se registran los modelos (tablas) para mostralo en el admin de Django

from.models import Categoria, Marca, Producto, Usuario, Cliente, Empleado, Inventario, Dimensiones, Venta, Historial, Fecha, Proveedores, OrdenCompra, Despacho, Direccion, Ciudad, Comuna, TipoPago, ComprobantePago, Cuenta, TipoUsuario


class ProductoAdmin(admin.ModelAdmin):
    list_display=["nombre_prod", "valor", "id_marca", "color"]
    list_editable=["valor"]
    search_fields=["nombre_prod"]
    list_filter=["id_marca", "color"]
    list_per_page=4



# Registrar modelos individuales
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin) #llamo la funcionalidad de filtros en el admin
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
admin.site.register(TipoUsuario)

#se modifica titulos del admin
admin.site.site_header = 'Administrador Larrain Webstore' #nombre del encabezado
admin.site.index_title = 'Panel de control Larrain Webstore' #nombre del título
admin.site.site_title = 'Administrador Larrain Webstore'