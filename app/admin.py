from django.contrib import admin
from.models import Categoria, Marca, Producto, Usuario, Cliente, Empleado, Inventario, Dimensiones, Venta, Historial, Fecha, Proveedores, OrdenCompra, Despacho, Direccion, Ciudad, Comuna, TipoPago, ComprobantePago, Cuenta, TipoUsuario

# se registran los modelos (tablas) para mostralo en el admin de Django




class ProductoAdmin(admin.ModelAdmin):
    list_display=["nombre_prod", "valor", "id_marca", "color"]
    list_editable=["valor"]
    search_fields=["nombre_prod"]
    list_filter=["id_marca", "color"]
    list_per_page=4



# Registrar modelos individuales

class ProductoAdmin(admin.ModelAdmin ):
    list_display = ["Nomber", "Precio", "Nuevo", "Marca"]
    list_editable = ["Precio"]
    search_fields = ["Nombre"]
    list_filter=["Marca","Nuevo"]
    list_per_page = 2

admin.site.register(Categoria)
admin.site.register(Marca)
<<<<<<< HEAD

admin.site.register(Producto)
=======
admin.site.register(Producto, ProductoAdmin) #llamo la funcionalidad de filtros en el admin
>>>>>>> webstore
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
