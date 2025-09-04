from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import (
    ImportadoraViewSet, BodegaViewSet, CategoriaViewSet, MarcaViewSet, ProductoViewSet,
    InventarioViewSet, DimensionesViewSet, HistorialViewSet, FechaViewSet, VentaViewSet,
    ComprobantePagoViewSet, TipoPagoViewSet, DebitoViewSet, CreditoViewSet, ProveedoresViewSet,
    ProductoListViewSet, InventarioDetalleViewSet
)

#crear router
router = DefaultRouter() #Crea automáticamente las URLs para operaciones CRUD

#registrar los viewsets con el router
#Conecta cada ViewSet con una URL base
router.register(r'importadoras', ImportadoraViewSet)
router.register(r'bodegas', BodegaViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'marcas', MarcaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'dimensiones', DimensionesViewSet)
router.register(r'historial', HistorialViewSet)
router.register(r'fechas', FechaViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'comprobantes-pago', ComprobantePagoViewSet)
router.register(r'tipos-pago', TipoPagoViewSet)
router.register(r'debitos', DebitoViewSet)
router.register(r'creditos', CreditoViewSet)
router.register(r'proveedores', ProveedoresViewSet)

# registrar los viewsets especiales de solo lectura
router.register(r'productos-list', ProductoListViewSet, basename='productos-list')
router.register(r'inventario-detalle', InventarioDetalleViewSet, basename='inventario-detalle')

# definir las URL
urlpatterns = [
    path('', include(router.urls)), #include(router.urls)= Incluye todas las rutas generadas
]


