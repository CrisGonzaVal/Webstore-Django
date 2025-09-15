from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import re
from decimal import Decimal

class CustomValidators:
    """
    Validadores personalizados para reglas de negocio específicas
    """
    
    @staticmethod
    def validar_rut_chileno(rut):
        """
        Validar RUT chileno con dígito verificador
        """
        if not rut:
            raise ValidationError("RUT es requerido")
        
        # Limpiar RUT
        rut = re.sub(r'[.-]', '', rut.upper())
        
        if len(rut) < 8 or len(rut) > 9:
            raise ValidationError("RUT debe tener entre 8 y 9 caracteres")
        
        # Separar número y dígito verificador
        numero = rut[:-1]
        dv = rut[-1]
        
        if not numero.isdigit():
            raise ValidationError("El número del RUT debe ser numérico")
        
        if dv not in '0123456789K':
            raise ValidationError("Dígito verificador inválido")
        
        # Calcular dígito verificador
        suma = 0
        multiplicador = 2
        
        for digito in reversed(numero):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        
        resto = suma % 11
        dv_calculado = 'K' if resto == 1 else ('0' if resto == 0 else str(11 - resto))
        
        if dv != dv_calculado:
            raise ValidationError("RUT inválido")
        
        return True
    
    @staticmethod
    def validar_precio_producto(precio):
        """
        Validar precio de producto según reglas de negocio
        """
        if not isinstance(precio, (int, float, Decimal)):
            raise ValidationError("Precio debe ser numérico")
        
        precio = Decimal(str(precio))
        
        if precio <= 0:
            raise ValidationError("El precio debe ser mayor a 0")
        
        if precio > Decimal('10000000'):  # 10 millones
            raise ValidationError("El precio no puede ser mayor a $10.000.000")
        
        return True
    
    @staticmethod
    def validar_stock(cantidad):
        """
        Validar cantidad de stock
        """
        if not isinstance(cantidad, int):
            raise ValidationError("Stock debe ser un número entero")
        
        if cantidad < 0:
            raise ValidationError("Stock no puede ser negativo")
        
        if cantidad > 99999:
            raise ValidationError("Stock no puede ser mayor a 99.999")
        
        return True
    
    @staticmethod
    def validar_email_cliente(email):
        """
        Validar email con reglas específicas
        """
        validator = EmailValidator()
        validator(email)
        
        # Reglas adicionales
        if '@' not in email:
            raise ValidationError("Email debe contener @")
        
        dominio = email.split('@')[1].lower()
        dominios_bloqueados = ['tempmail.com', '10minutemail.com']
        
        if dominio in dominios_bloqueados:
            raise ValidationError("Dominio de email no permitido")
        
        return True
    
    @staticmethod
    def validar_telefono_chileno(telefono):
        """
        Validar teléfono chileno
        """
        if not telefono:
            return True  # Opcional
        
        # Limpiar teléfono
        telefono_limpio = re.sub(r'[^\d+]', '', telefono)
        
        # Formatos válidos: +56912345678, 56912345678, 912345678
        patrones = [
            r'^\+56[2-9]\d{8}$',     # +56 + móvil
            r'^56[2-9]\d{8}$',       # 56 + móvil
            r'^[2-9]\d{8}$',         # móvil directo
            r'^\+56[2-7]\d{7}$',     # +56 + fijo
            r'^56[2-7]\d{7}$',       # 56 + fijo
            r'^[2-7]\d{7}$'          # fijo directo
        ]
        
        if not any(re.match(patron, telefono_limpio) for patron in patrones):
            raise ValidationError("Formato de teléfono chileno inválido")
        
        return True