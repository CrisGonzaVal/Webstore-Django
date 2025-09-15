from django.core.exceptions import ValidationError
from decimal import Decimal
from .InventarioService import InventarioService
from ..models import Producto

class CarritoService:
    """
    Servicio para manejar la lógica de negocio del carrito
    Migrado desde Carrito.py para centralizar la lógica
    """
    
    @staticmethod
    def validar_producto_disponible(producto_id, cantidad=1):
        """
        Validar que el producto esté disponible para agregar al carrito
        """
        try:
            producto = Producto.objects.get(id_producto=producto_id)
        except Producto.DoesNotExist:
            raise ValidationError("Producto no encontrado")
        
        if not InventarioService.verificar_disponibilidad(producto_id, cantidad):
            raise ValidationError("Producto no disponible o sin stock suficiente")
        
        return producto
    
    @staticmethod
    def calcular_subtotal(producto, cantidad):
        """
        Calcular subtotal con validaciones
        """
        if cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor a 0")
        
        # Regla de negocio: máximo 10 unidades por producto
        if cantidad > 10:
            raise ValidationError("Máximo 10 unidades por producto")
        
        return producto.valor * cantidad
    
    @staticmethod
    def aplicar_descuentos(total_carrito, codigo_descuento=None):
        """
        Aplicar descuentos según reglas de negocio
        """
        descuento = Decimal('0.00')
        
        # Regla: descuento por volumen
        if total_carrito >= 100000:  # Más de $100.000
            descuento = total_carrito * Decimal('0.10')  # 10% descuento
        elif total_carrito >= 50000:  # Más de $50.000
            descuento = total_carrito * Decimal('0.05')   # 5% descuento
        
        # Regla: códigos de descuento especiales
        if codigo_descuento:
            descuento_codigo = CarritoService._validar_codigo_descuento(codigo_descuento, total_carrito)
            descuento = max(descuento, descuento_codigo)
        
        return descuento
    
    @staticmethod
    def _validar_codigo_descuento(codigo, total):
        """
        Validar códigos de descuento
        """
        codigos_validos = {
            'PRIMERA_COMPRA': Decimal('0.15'),  # 15% primera compra
            'CLIENTE_VIP': Decimal('0.20'),     # 20% cliente VIP
            'DESCUENTO10': Decimal('0.10'),     # 10% descuento general
        }
        
        if codigo in codigos_validos:
            return total * codigos_validos[codigo]
        
        return Decimal('0.00')
    
    @staticmethod
    def calcular_envio(total_carrito, region='metropolitana'):
        """
        Calcular costo de envío según reglas de negocio
        """
        # Regla: envío gratis sobre cierto monto
        if total_carrito >= 50000:
            return Decimal('0.00')
        
        # Costos por región
        costos_envio = {
            'metropolitana': Decimal('5000'),
            'valparaiso': Decimal('7000'),
            'otras_regiones': Decimal('10000'),
        }
        
        return costos_envio.get(region, costos_envio['otras_regiones'])