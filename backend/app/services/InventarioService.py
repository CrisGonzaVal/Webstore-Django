from django.core.exceptions import ValidationError
from django.db import transaction
from ..models import Inventario, Producto, Historial
from datetime import datetime

class InventarioService:
    """
    Servicio para manejar la lógica de negocio del inventario
    """
    
    @staticmethod
    def verificar_disponibilidad(producto_id, cantidad_solicitada):
        """
        Verificar si hay stock suficiente
        """
        try:
            inventario = Inventario.objects.get(id_producto=producto_id)
        except Inventario.DoesNotExist:
            return False
        
        return (inventario.cantidad >= cantidad_solicitada and 
                inventario.estatus == 'disponible')
    
    @staticmethod
    @transaction.atomic
    def reducir_stock(producto_id, cantidad, motivo="venta"):
        """
        Reducir stock con validaciones y registro de historial
        """
        try:
            inventario = Inventario.objects.select_for_update().get(id_producto=producto_id)
        except Inventario.DoesNotExist:
            raise ValidationError("No existe inventario para este producto")
        
        if inventario.cantidad < cantidad:
            raise ValidationError(f"Stock insuficiente. Disponible: {inventario.cantidad}")
        
        if inventario.estatus != 'disponible':
            raise ValidationError("Producto no disponible")
        
        # Reducir stock
        inventario.cantidad -= cantidad
        
        # Regla de negocio: cambiar estatus si stock bajo
        if inventario.cantidad <= 5:
            inventario.estatus = 'stock_bajo'
        
        if inventario.cantidad <= 0:
            inventario.estatus = 'agotado'
        
        inventario.save()
        
        # Registrar en historial
        InventarioService._registrar_movimiento(
            producto_id, 
            f"Reducción de stock: -{cantidad} - Motivo: {motivo}"
        )
        
        return inventario
    
    @staticmethod
    @transaction.atomic
    def aumentar_stock(producto_id, cantidad, motivo="reposición"):
        """
        Aumentar stock con registro de historial
        """
        try:
            inventario = Inventario.objects.select_for_update().get(id_producto=producto_id)
        except Inventario.DoesNotExist:
            # Crear inventario si no existe
            producto = Producto.objects.get(id_producto=producto_id)
            inventario = Inventario.objects.create(
                id_producto=producto,
                cantidad=cantidad,
                ubicacion='bodega_principal',
                estatus='disponible'
            )
        else:
            # Aumentar stock existente
            inventario.cantidad += cantidad
            
            # Actualizar estatus
            if inventario.cantidad > 5:
                inventario.estatus = 'disponible'
            
            inventario.save()
        
        # Registrar en historial
        InventarioService._registrar_movimiento(
            producto_id, 
            f"Aumento de stock: +{cantidad} - Motivo: {motivo}"
        )
        
        return inventario
    
    @staticmethod
    def _registrar_movimiento(producto_id, accion):
        """
        Registrar movimiento en el historial
        """
        try:
            producto = Producto.objects.get(id_producto=producto_id)
            Historial.objects.create(
                id_producto=producto,
                accion=accion
            )
        except Exception as e:
            # Log error pero no fallar la operación principal
            pass
    
    @staticmethod
    def obtener_productos_stock_bajo(limite=5):
        """
        Obtener productos con stock bajo
        """
        return Inventario.objects.filter(
            cantidad__lte=limite,
            estatus__in=['disponible', 'stock_bajo']
        ).select_related('id_producto')
    
    @staticmethod
    def obtener_valor_inventario_total():
        """
        Calcular valor total del inventario
        """
        inventarios = Inventario.objects.select_related('id_producto').filter(
            cantidad__gt=0
        )
        
        total = sum(
            inv.cantidad * inv.id_producto.valor 
            for inv in inventarios
        )
        
        return total