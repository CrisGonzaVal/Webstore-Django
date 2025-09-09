from decimal import Decimal
from django.core.exceptions import ValidationError
from ..services.CarritoService import CarritoService
from ..services.InventarioService import InventarioService
import logging

logger = logging.getLogger(__name__)

class CarritoSesion:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.carrito = self.session.get("carrito")
        if not self.carrito:
            self.carrito = self.session["carrito"] = {}

    def agregar(self, producto, cantidad=1):
        #Agregar producto al carrito con validaciones de negocio
        
        try:
            # 1. Validar con CarritoService
            CarritoService.validar_producto_disponible(
                producto.id_producto, 
                cantidad
            )
            
            id = str(producto.id_producto)
            
            if id not in self.carrito:
                # Nuevo producto en carrito
                subtotal = CarritoService.calcular_subtotal(producto, cantidad)
                
                self.carrito[id] = {
                    "producto_id": producto.id_producto,
                    "nombre": producto.nombre_prod,
                    "acumulado": str(subtotal),
                    "cantidad": cantidad,
                    "imagen": producto.imagen.url if producto.imagen else "",
                    "color": getattr(producto, 'color', ''),
                    "id_marca": str(producto.id_marca),
                    "precio_unitario": str(producto.valor)
                }
            else:
                # Producto ya existe, aumentar cantidad
                nueva_cantidad = self.carrito[id]["cantidad"] + cantidad
                
                # Validar nueva cantidad total
                CarritoService.validar_producto_disponible(
                    producto.id_producto, 
                    nueva_cantidad
                )
                
                # Calcular nuevo subtotal
                nuevo_subtotal = CarritoService.calcular_subtotal(producto, nueva_cantidad)
                
                self.carrito[id]["cantidad"] = nueva_cantidad
                self.carrito[id]["acumulado"] = str(nuevo_subtotal)
            
            self.guardar_carrito()
            return True, "Producto agregado correctamente"
            
        except ValidationError as e:
            logger.warning(f"Error al agregar producto {producto.id_producto}: {str(e)}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Error inesperado al agregar producto {producto.id_producto}: {str(e)}")
            return False, "Error interno del servidor"

    def disminuir(self, producto):
        """
        Disminuir cantidad de producto con validaciones
        """
        try:
            id = str(producto.id_producto)
            
            if id in self.carrito:
                if self.carrito[id]["cantidad"] > 1:
                    nueva_cantidad = self.carrito[id]["cantidad"] - 1
                    nuevo_subtotal = CarritoService.calcular_subtotal(producto, nueva_cantidad)
                    
                    self.carrito[id]["cantidad"] = nueva_cantidad
                    self.carrito[id]["acumulado"] = str(nuevo_subtotal)
                else:
                    # Si cantidad es 1, eliminar producto
                    self.eliminar(producto)
                    return True, "Producto eliminado del carrito"
                
                self.guardar_carrito()
                return True, "Cantidad actualizada"
            else:
                return False, "Producto no encontrado en el carrito"
                
        except Exception as e:
            logger.error(f"Error al disminuir producto {producto.id_producto}: {str(e)}")
            return False, "Error al actualizar carrito"

    def eliminar(self, producto):
        """
        Eliminar producto del carrito
        """
        try:
            id = str(producto.id_producto)
            if id in self.carrito:
                del self.carrito[id]
                self.guardar_carrito()
                return True, "Producto eliminado correctamente"
            else:
                return False, "Producto no encontrado en el carrito"
        except Exception as e:
            logger.error(f"Error al eliminar producto {producto.id_producto}: {str(e)}")
            return False, "Error al eliminar producto"

    def actualizar_cantidad(self, producto, nueva_cantidad):
        """
        Actualizar cantidad específica de un producto
        """
        try:
            # Validar nueva cantidad
            CarritoService.validar_producto_disponible(
                producto.id_producto, 
                nueva_cantidad
            )
            
            id = str(producto.id_producto)
            
            if id in self.carrito:
                if nueva_cantidad <= 0:
                    return self.eliminar(producto)
                
                nuevo_subtotal = CarritoService.calcular_subtotal(producto, nueva_cantidad)
                
                self.carrito[id]["cantidad"] = nueva_cantidad
                self.carrito[id]["acumulado"] = str(nuevo_subtotal)
                
                self.guardar_carrito()
                return True, "Cantidad actualizada correctamente"
            else:
                return False, "Producto no encontrado en el carrito"
                
        except ValidationError as e:
            return False, str(e)
        except Exception as e:
            logger.error(f"Error al actualizar cantidad {producto.id_producto}: {str(e)}")
            return False, "Error al actualizar cantidad"

    def limpiar(self):
        """
        Limpiar carrito completamente
        """
        try:
            self.session["carrito"] = {}
            self.session.modified = True
            return True, "Carrito limpiado correctamente"
        except Exception as e:
            logger.error(f"Error al limpiar carrito: {str(e)}")
            return False, "Error al limpiar carrito"

    def obtener_total_items(self):
        """
        Obtener total de items en el carrito
        """
        return sum(item['cantidad'] for item in self.carrito.values())

    def obtener_total_sin_descuentos(self):
        """
        Obtener total sin aplicar descuentos
        """
        total = Decimal('0.00')
        for item in self.carrito.values():
            total += Decimal(str(item["acumulado"]))
        return total

    def obtener_total_con_descuentos(self, codigo_descuento=None):
        """
        Obtener total aplicando descuentos usando CarritoService
        """
        try:
            total_sin_descuentos = self.obtener_total_sin_descuentos()
            
            if total_sin_descuentos == 0:
                return Decimal('0.00')
            
            descuentos = CarritoService.aplicar_descuentos(
                total_sin_descuentos, 
                codigo_descuento
            )
            
            return total_sin_descuentos - descuentos
            
        except Exception as e:
            logger.error(f"Error al calcular total con descuentos: {str(e)}")
            return self.obtener_total_sin_descuentos()

    def obtener_costo_envio(self, region='metropolitana'):
        """
        Obtener costo de envío usando CarritoService
        """
        try:
            total_carrito = self.obtener_total_con_descuentos()
            return CarritoService.calcular_envio(total_carrito, region)
        except Exception as e:
            logger.error(f"Error al calcular envío: {str(e)}")
            return Decimal('5000.00')  # Costo default

    def obtener_resumen_carrito(self, codigo_descuento=None, region='metropolitana'):
        """
        Obtener resumen completo del carrito
        """
        subtotal = self.obtener_total_sin_descuentos()
        total_con_descuentos = self.obtener_total_con_descuentos(codigo_descuento)
        descuentos = subtotal - total_con_descuentos
        envio = self.obtener_costo_envio(region)
        total_final = total_con_descuentos + envio
        
        return {
            'items': len(self.carrito),
            'cantidad_total': self.obtener_total_items(),
            'subtotal': subtotal,
            'descuentos': descuentos,
            'envio': envio,
            'total': total_final,
            'productos': list(self.carrito.values())
        }

    def validar_carrito_completo(self):
        """
        Validar todo el carrito antes del checkout
        """
        errores = []
        
        if not self.carrito:
            return False, ["El carrito está vacío"]
        
        for item in self.carrito.values():
            try:
                # Verificar disponibilidad de cada producto
                if not InventarioService.verificar_disponibilidad(
                    item['producto_id'], 
                    item['cantidad']
                ):
                    errores.append(f"Producto '{item['nombre']}' no tiene stock suficiente")
            except Exception as e:
                errores.append(f"Error al validar producto '{item['nombre']}'")
        
        if errores:
            return False, errores
        
        return True, ["Carrito válido"]

    def convertir_para_venta(self):
        """
        Convertir carrito a formato para VentaService
        """
        items_venta = []
        
        for item in self.carrito.values():
            items_venta.append({
                'producto_id': item['producto_id'],
                'cantidad': item['cantidad'],
                'precio_unitario': Decimal(item['precio_unitario']),
                'subtotal': Decimal(item['acumulado'])
            })
        
        return items_venta

    def guardar_carrito(self):
        """
        Guardar carrito en sesión
        """
        self.session["carrito"] = self.carrito
        self.session.modified = True