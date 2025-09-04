from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from datetime import datetime
from ..models import Venta, Producto, ComprobantePago, TipoPago
from .InventarioService import InventarioService
from .CarritoService import CarritoService

class VentaService:
    """
    Servicio para manejar la lógica de negocio de ventas
    """
    
    @staticmethod
    @transaction.atomic
    def procesar_venta(items_carrito, datos_cliente, metodo_pago):
        """
        Procesar una venta completa con todas las validaciones
        """
        # Validar datos de entrada
        VentaService._validar_datos_venta(items_carrito, datos_cliente, metodo_pago)
        
        # Calcular totales
        subtotal = VentaService._calcular_subtotal(items_carrito)
        descuentos = CarritoService.aplicar_descuentos(subtotal)
        envio = CarritoService.calcular_envio(subtotal - descuentos)
        total = subtotal - descuentos + envio
        
        # Verificar disponibilidad de todos los productos
        for item in items_carrito:
            if not InventarioService.verificar_disponibilidad(
                item['producto_id'], 
                item['cantidad']
            ):
                producto = Producto.objects.get(id_producto=item['producto_id'])
                raise ValidationError(f"Producto '{producto.nombre_prod}' no disponible")
        
        # Crear venta
        venta = Venta.objects.create(
            subtotal=subtotal,
            descuentos=descuentos,
            costo_envio=envio,
            total=total,
            estado='pendiente',
            datos_cliente=datos_cliente
        )
        
        # Reducir stock de todos los productos
        for item in items_carrito:
            InventarioService.reducir_stock(
                item['producto_id'],
                item['cantidad'],
                f"Venta #{venta.id}"
            )
        
        # Procesar pago
        comprobante = VentaService._procesar_pago(venta, metodo_pago)
        
        # Actualizar estado de venta
        venta.estado = 'confirmada'
        venta.fecha_confirmacion = datetime.now()
        venta.save()
        
        return {
            'venta': venta,
            'comprobante': comprobante,
            'total': total
        }
    
    @staticmethod
    def _validar_datos_venta(items_carrito, datos_cliente, metodo_pago):
        """
        Validar datos necesarios para procesar venta
        """
        if not items_carrito:
            raise ValidationError("El carrito está vacío")
        
        if not datos_cliente.get('email'):
            raise ValidationError("Email del cliente es requerido")
        
        if not datos_cliente.get('nombre'):
            raise ValidationError("Nombre del cliente es requerido")
        
        if metodo_pago not in ['efectivo', 'tarjeta', 'transferencia', 'paypal']:
            raise ValidationError("Método de pago no válido")
    
    @staticmethod
    def _calcular_subtotal(items_carrito):
        """
        Calcular subtotal de todos los items
        """
        subtotal = Decimal('0.00')
        
        for item in items_carrito:
            try:
                producto = Producto.objects.get(id_producto=item['producto_id'])
                item_subtotal = CarritoService.calcular_subtotal(
                    producto, 
                    item['cantidad']
                )
                subtotal += item_subtotal
            except Producto.DoesNotExist:
                raise ValidationError(f"Producto {item['producto_id']} no encontrado")
        
        return subtotal
    
    @staticmethod
    def _procesar_pago(venta, metodo_pago):
        """
        Procesar el pago según el método elegido
        """
        # Obtener tipo de pago
        try:
            tipo_pago = TipoPago.objects.get(nombre=metodo_pago)
        except TipoPago.DoesNotExist:
            raise ValidationError(f"Tipo de pago '{metodo_pago}' no configurado")
        
        # Crear comprobante de pago
        comprobante = ComprobantePago.objects.create(
            venta=venta,
            tipo_pago=tipo_pago,
            monto=venta.total,
            estado='procesando'
        )
        
        # Lógica específica por método de pago
        if metodo_pago == 'paypal':
            # Integrar con PayPal API
            comprobante = VentaService._procesar_paypal(comprobante)
        elif metodo_pago == 'tarjeta':
            # Integrar con procesador de tarjetas
            comprobante = VentaService._procesar_tarjeta(comprobante)
        else:
            # Métodos manuales
            comprobante.estado = 'pendiente_confirmacion'
            comprobante.save()
        
        return comprobante
    
    @staticmethod
    def _procesar_paypal(comprobante):
        """
        Procesar pago con PayPal
        """
        # Aquí iría la integración real con PayPal
        # Por ahora simulamos el proceso
        comprobante.estado = 'aprobado'
        comprobante.referencia_externa = f"PAYPAL_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        comprobante.save()
        return comprobante
    
    @staticmethod
    def _procesar_tarjeta(comprobante):
        """
        Procesar pago con tarjeta
        """
        # Aquí iría la integración con procesador de tarjetas
        comprobante.estado = 'aprobado'
        comprobante.referencia_externa = f"CARD_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        comprobante.save()
        return comprobante
    
    @staticmethod
    def cancelar_venta(venta_id, motivo="Cancelación por cliente"):
        """
        Cancelar una venta y restaurar stock
        """
        try:
            venta = Venta.objects.get(id=venta_id)
        except Venta.DoesNotExist:
            raise ValidationError("Venta no encontrada")
        
        if venta.estado == 'cancelada':
            raise ValidationError("La venta ya está cancelada")
        
        if venta.estado == 'entregada':
            raise ValidationError("No se puede cancelar una venta ya entregada")
        
        # Restaurar stock (lógica simplificada)
        # En un caso real, necesitarías los items de la venta
        venta.estado = 'cancelada'
        venta.motivo_cancelacion = motivo
        venta.fecha_cancelacion = datetime.now()
        venta.save()
        
        return venta
    
    @staticmethod
    def obtener_reportes_ventas(fecha_inicio=None, fecha_fin=None):
        """
        Generar reportes de ventas
        """
        queryset = Venta.objects.filter(estado='confirmada')
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_creacion__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(fecha_creacion__lte=fecha_fin)
        
        total_ventas = queryset.count()
        total_ingresos = sum(venta.total for venta in queryset)
        promedio_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
        
        return {
            'total_ventas': total_ventas,
            'total_ingresos': total_ingresos,
            'promedio_venta': promedio_venta,
            'ventas': queryset.order_by('-fecha_creacion')
        }