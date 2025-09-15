from rest_framework import viewsets # automáticamente proporciona operaciones CRUD completas
from rest_framework.permissions import IsAuthenticated
from ..models import (
    Importadora, Bodega, Categoria, Marca, Producto, 
    Inventario, Dimensiones, Historial, Fecha, Venta, 
    ComprobantePago, TipoPago, Debito, Credito, Proveedores
)
from .serializers import (
    ImportadoraSerializer, BodegaSerializer, CategoriaSerializer, MarcaSerializer, ProductoSerializer,
    InventarioSerializer, DimensionesSerializer, HistorialSerializer, FechaSerializer, VentaSerializer,
    ComprobantePagoSerializer, TipoPagoSerializer, DebitoSerializer, CreditoSerializer, ProveedoresSerializer,
    ProductoListSerializer, InventarioDetalleSerializer
)

from django_filters.rest_framework import DjangoFilterBackend #para filtros en la API
from rest_framework.permissions import AllowAny # Permitir acceso sin autenticación

class ImportadoraViewSet(viewsets.ModelViewSet):
    queryset = Importadora.objects.all() #define qué datos obtener de la base de datos
    serializer_class = ImportadoraSerializer #define cómo convertir los datos
    # permission_classes = [AllowAny] opcional por ahora

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
class MarcaViewSet(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    filter_backends = [DjangoFilterBackend] # Habilitar filtros
    filterset_fields = ['id_categoria', 'id_marca', 'valor']
    search_fields = ['nombre_prod', 'descripcion']
    ordering_fields = ['valor', 'nombre_prod']
    """ Filtrar por categoría
        GET /api/productos/?id_categoria=2

        Filtrar por marca
        GET /api/productos/?id_marca=5

        Filtrar por precio exacto
        GET /api/productos/?valor=15000

        http://localhost:8000/api/productos/?search=laptop # Buscar por nombre o descripción
        http://localhost:8000/api/productos/?ordering=valor  # Ordenar por precio ascendente
        http://localhost:8000/api/productos/?ordering=-valor # Ordenar por precio descendente
    """

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class DimensionesViewSet(viewsets.ModelViewSet):
    queryset = Dimensiones.objects.all()
    serializer_class = DimensionesSerializer

class HistorialViewSet(viewsets.ModelViewSet):
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer

class FechaViewSet(viewsets.ModelViewSet):
    queryset = Fecha.objects.all()
    serializer_class = FechaSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class ComprobantePagoViewSet(viewsets.ModelViewSet):
    queryset = ComprobantePago.objects.all()
    serializer_class = ComprobantePagoSerializer

class TipoPagoViewSet(viewsets.ModelViewSet):
    queryset = TipoPago.objects.all()
    serializer_class = TipoPagoSerializer

class DebitoViewSet(viewsets.ModelViewSet):
    queryset = Debito.objects.all()
    serializer_class = DebitoSerializer

class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer

class ProveedoresViewSet(viewsets.ModelViewSet):
    queryset = Proveedores.objects.all()
    serializer_class = ProveedoresSerializer

class ProductoListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoListSerializer

class InventarioDetalleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioDetalleSerializer


class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer

