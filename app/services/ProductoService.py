from django.core.exceptions import ValidationError
from ..models import Producto, Categoria, Marca, Inventario
from decimal import Decimal

class ProductoService:
    """
    Servicio para manejar la lógica de negocio de productos
    """
    
    @staticmethod
    def crear_producto(data):
        """
        Crear un producto con validaciones de negocio
        """
        # Regla de negocio: precio mínimo
        if data.get('valor', 0) <= 0:
            raise ValidationError("El precio debe ser mayor a 0")
        
        # Regla de negocio: nombre único por categoría
        if Producto.objects.filter(
            nombre_prod=data.get('nombre_prod'),
            id_categoria=data.get('id_categoria')
        ).exists():
            raise ValidationError("Ya existe un producto con ese nombre en la categoría")
        
        return Producto.objects.create(**data)
    
    @staticmethod
    def actualizar_precio(producto_id, nuevo_precio):
        """
        Actualizar precio con validaciones de negocio
        """
        try:
            producto = Producto.objects.get(id_producto=producto_id)
        except Producto.DoesNotExist:
            raise ValidationError("Producto no encontrado")
        
        nuevo_precio = Decimal(str(nuevo_precio))
        
        # Regla de negocio: no permitir descuentos mayores al 70%
        precio_minimo = producto.valor * Decimal('0.3')
        if nuevo_precio < precio_minimo:
            raise ValidationError("No se permite descuento mayor al 70%")
        
        # Regla de negocio: no permitir aumentos mayores al 200%
        precio_maximo = producto.valor * Decimal('3.0')
        if nuevo_precio > precio_maximo:
            raise ValidationError("No se permite aumento mayor al 200%")
        
        producto.valor = nuevo_precio
        producto.save()
        return producto
    
    @staticmethod
    def obtener_productos_por_categoria(categoria_id):
        """
        Obtener productos por categoría con validaciones
        """
        try:
            categoria = Categoria.objects.get(id_categoria=categoria_id)
        except Categoria.DoesNotExist:
            raise ValidationError("Categoría no encontrada")
        
        return Producto.objects.filter(id_categoria=categoria)
    
    @staticmethod
    def obtener_productos_disponibles():
        """
        Obtener solo productos que tienen stock disponible
        """
        return Producto.objects.filter(
            inventario__cantidad__gt=0,
            inventario__estatus='disponible'
        )