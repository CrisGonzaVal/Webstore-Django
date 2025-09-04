#Los serializers son componentes que convierten datos entre diferentes formatos. json a modelo y modelo a json

from rest_framework import serializers
from ..models import (
    Importadora, Bodega, Categoria, Marca, Producto, 
    Inventario, Dimensiones, Historial, Fecha, Venta, 
    ComprobantePago, TipoPago, Debito, Credito, Proveedores
)


class ImportadoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importadora
        fields = '__all__'


class BodegaSerializer(serializers.ModelSerializer):
    rut_empresa_nombre = serializers.CharField(source='rut_empresa.rut_empresa', read_only=True)
    
    class Meta:
        model = Bodega
        fields = ['id_bodega', 'rut_empresa', 'rut_empresa_nombre']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='id_categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='id_marca.nombre_m', read_only=True)
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = [
            'id_producto', 'nombre_prod', 'descripcion', 'valor', 'color',
            'id_categoria', 'categoria_nombre', 'id_marca', 'marca_nombre',
            'imagen', 'imagen_url'
        ]
    
    def get_imagen_url(self, obj):
        if obj.imagen:
            return obj.imagen.url
        return None


class InventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='id_producto.nombre_prod', read_only=True)
    producto_valor = serializers.DecimalField(source='id_producto.valor', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Inventario
        fields = [
            'id_inventario', 'id_producto', 'producto_nombre', 'producto_valor',
            'cantidad', 'ubicacion', 'estatus'
        ]


class DimensionesSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='id_producto.nombre_prod', read_only=True)
    
    class Meta:
        model = Dimensiones
        fields = ['id_producto', 'producto_nombre', 'alto', 'largo', 'ancho', 'peso']


class HistorialSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='id_producto.nombre_prod', read_only=True)
    
    class Meta:
        model = Historial
        fields = ['id_registro', 'id_producto', 'producto_nombre', 'accion']


class FechaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fecha
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='id_producto.nombre_prod', read_only=True)
    producto_valor = serializers.DecimalField(source='id_producto.valor', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Venta
        fields = ['id_venta', 'id_producto', 'producto_nombre', 'producto_valor']


class ComprobantePagoSerializer(serializers.ModelSerializer):
    venta_producto = serializers.CharField(source='id_venta.id_producto.nombre_prod', read_only=True)
    
    class Meta:
        model = ComprobantePago
        fields = ['id_comprobante', 'id_venta', 'venta_producto']


class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'


class DebitoSerializer(serializers.ModelSerializer):
    banco = serializers.CharField(source='id_n_tarjeta.banco', read_only=True)
    
    class Meta:
        model = Debito
        fields = ['id_n_tarjeta', 'banco']


class CreditoSerializer(serializers.ModelSerializer):
    banco = serializers.CharField(source='id_n_tarjeta.banco', read_only=True)
    
    class Meta:
        model = Credito
        fields = ['id_n_tarjeta', 'banco']


class ProveedoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedores
        fields = '__all__'


# Serializers especiales 

class ProductoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listado de productos"""
    categoria_nombre = serializers.CharField(source='id_categoria.nombre', read_only=True)
    marca_nombre = serializers.CharField(source='id_marca.nombre_m', read_only=True)
    imagen_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Producto
        fields = [
            'id_producto', 'nombre_prod', 'valor', 'color',
            'categoria_nombre', 'marca_nombre', 'imagen_url'
        ]
    
    def get_imagen_url(self, obj):
        if obj.imagen:
            return obj.imagen.url
        return None


class InventarioDetalleSerializer(serializers.ModelSerializer):
    """Serializer detallado para inventario con información completa del producto"""
    producto = ProductoSerializer(source='id_producto', read_only=True)
    
    class Meta:
        model = Inventario
        fields = ['id_inventario', 'producto', 'cantidad', 'ubicacion', 'estatus']
