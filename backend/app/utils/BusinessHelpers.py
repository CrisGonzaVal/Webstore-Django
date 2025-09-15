from decimal import Decimal
import re
from datetime import datetime, timedelta

class BusinessHelpers:
    """
    Funciones helper para lógica de negocio común
    """
    
    @staticmethod
    def formatear_precio_chileno(precio):
        """
        Formatear precio en formato chileno: $1.234.567
        """
        if not precio:
            return "$0"
        
        precio = int(precio)
        return f"${precio:,}".replace(',', '.')
    
    @staticmethod
    def calcular_cuotas(precio_total, numero_cuotas):
        """
        Calcular valor de cuotas sin interés
        """
        if numero_cuotas <= 0:
            raise ValueError("Número de cuotas debe ser mayor a 0")
        
        precio_decimal = Decimal(str(precio_total))
        cuota = precio_decimal / numero_cuotas
        
        # Redondear a peso más cercano
        return cuota.quantize(Decimal('0'))
    
    @staticmethod
    def generar_codigo_orden():
        """
        Generar código único para órdenes
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"ORD-{timestamp}"
    
    @staticmethod
    def calcular_fecha_entrega(dias_habiles=5):
        """
        Calcular fecha estimada de entrega
        """
        fecha_actual = datetime.now().date()
        dias_agregados = 0
        
        while dias_agregados < dias_habiles:
            fecha_actual += timedelta(days=1)
            # Saltar fines de semana (lunes=0, domingo=6)
            if fecha_actual.weekday() < 5:  # 0-4 = lunes a viernes
                dias_agregados += 1
        
        return fecha_actual
    
    @staticmethod
    def limpiar_texto_busqueda(texto):
        """
        Limpiar texto para búsquedas
        """
        if not texto:
            return ""
        
        # Remover caracteres especiales y normalizar
        texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
        texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
        
        return texto_limpio
    
    @staticmethod
    def convertir_peso_a_usd(peso_chileno, tasa_cambio=None):
        """
        Convertir peso chileno a dólar
        """
        if not tasa_cambio:
            # En producción, esto debería venir de una API de tasas de cambio
            tasa_cambio = Decimal('800')  # Tasa ejemplo
        
        peso_decimal = Decimal(str(peso_chileno))
        usd = peso_decimal / tasa_cambio
        
        return usd.quantize(Decimal('0.01'))  # 2 decimales
    
    @staticmethod
    def validar_horario_atencion():
        """
        Verificar si estamos en horario de atención
        """
        ahora = datetime.now()
        hora_actual = ahora.time()
        
        # Horario: 9:00 a 18:00, lunes a viernes
        if ahora.weekday() >= 5:  # Sábado o domingo
            return False
        
        from datetime import time
        if time(9, 0) <= hora_actual <= time(18, 0):
            return True
        
        return False