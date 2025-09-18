from django.core.exceptions import ValidationError
import re
import logging

logger = logging.getLogger(__name__)

class RutValidationService:
    """
    Servicio dedicado exclusivamente a la validación y manejo de RUTs chilenos
    """
    
    @staticmethod
    def limpiar_rut(rut):
        """
        Limpia el RUT eliminando puntos, guiones y espacios
        Retorna: (numero, dv) como tupla
        """
        if not rut:
            raise ValidationError("RUT no puede estar vacío")
        
        # Eliminar puntos, guiones y espacios
        rut_limpio = re.sub(r'[.\-\s]', '', str(rut).upper().strip())
        
        if len(rut_limpio) < 2:
            raise ValidationError("RUT debe tener al menos 2 caracteres")
        
        # Separar número y dígito verificador
        numero = rut_limpio[:-1]
        dv = rut_limpio[-1]
        
        return numero, dv
    
    @staticmethod
    def validar_formato_rut(rut):
        """
        Valida que el RUT tenga el formato correcto
        """
        try:
            numero, dv = RutValidationService.limpiar_rut(rut)
            
            # Validar que el número sea numérico
            if not numero.isdigit():
                raise ValidationError("El número del RUT debe contener solo dígitos")
            
            # Validar longitud del número (7-8 dígitos para personas naturales)
            if len(numero) < 7 or len(numero) > 8:
                raise ValidationError("El RUT debe tener entre 7 y 8 dígitos")
            
            # Validar dígito verificador (0-9 o K)
            if dv not in '0123456789K':
                raise ValidationError("El dígito verificador debe ser un número del 0-9 o K")
            
            return numero, dv
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validando formato RUT: {str(e)}")
            raise ValidationError("Formato de RUT inválido")
    
    @staticmethod
    def calcular_digito_verificador(numero):
        """
        Calcula el dígito verificador de un RUT
        """
        if not numero or not numero.isdigit():
            raise ValidationError("Número de RUT inválido para calcular DV")
        
        suma = 0
        multiplicador = 2
        
        # Calcular suma ponderada
        for digito in reversed(numero):
            suma += int(digito) * multiplicador
            multiplicador = multiplicador + 1 if multiplicador < 7 else 2
        
        # Calcular dígito verificador
        resto = suma % 11
        if resto < 2:
            return str(resto)
        else:
            return 'K' if resto == 1 else str(11 - resto)
    
    @staticmethod
    def validar_rut_completo(rut):
        """
        Valida completamente un RUT (formato + dígito verificador)
        """
        try:
            numero, dv_ingresado = RutValidationService.validar_formato_rut(rut)
            
            # Calcular dígito verificador correcto
            dv_calculado = RutValidationService.calcular_digito_verificador(numero)
            
            # Verificar que coincidan
            if dv_ingresado.upper() != dv_calculado.upper():
                raise ValidationError("El dígito verificador del RUT es incorrecto")
            
            logger.info(f"RUT validado exitosamente: {numero}-{dv_calculado}")
            return numero, dv_calculado
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error validando RUT completo: {str(e)}")
            raise ValidationError("Error interno validando RUT")
    
    @staticmethod
    def formatear_rut(numero, dv):
        """
        Formatea el RUT con puntos y guión
        """
        if not numero or not dv:
            return ""
        
        if len(numero) == 7:
            return f"{numero[:1]}.{numero[1:4]}.{numero[4:]}-{dv}"
        elif len(numero) == 8:
            return f"{numero[:2]}.{numero[2:5]}.{numero[5:]}-{dv}"
        else:
            return f"{numero}-{dv}"
    
    @staticmethod
    def normalizar_rut(rut):
        """
        Normaliza un RUT: lo valida y retorna en formato estándar
        """
        numero, dv = RutValidationService.validar_rut_completo(rut)
        return {
            'numero': numero,
            'dv': dv,
            'rut_sin_formato': numero + dv,
            'rut_formateado': RutValidationService.formatear_rut(numero, dv)
        }