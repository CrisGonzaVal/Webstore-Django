from django.core.exceptions import ValidationError
from ..models import Usuario, TipoUsuario
from .RutValidationService import RutValidationService
import logging
import re

logger = logging.getLogger(__name__)

class UsuarioValidationService:
    """
    Servicio para validaciones específicas de Usuario
    """
    
    @staticmethod
    def validar_email(email):
        """
        Valida formato de email
        """
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError("Formato de email inválido")
        
        # Verificar si ya existe
        if Usuario.objects.filter(email=email).exists():
            raise ValidationError("El email ya está registrado")
        
        return email.lower().strip()
    
    @staticmethod
    def validar_edad(edad):
        """
        Valida que la edad sea válida
        """
        try:
            edad = int(edad)
            if edad < 18:
                raise ValidationError("Debe ser mayor de 18 años")
            if edad > 120:
                raise ValidationError("Edad no válida")
            return edad
        except (ValueError, TypeError):
            raise ValidationError("La edad debe ser un número válido")
    
    @staticmethod
    def validar_nombre(nombre, campo="nombre"):
        """
        Valida nombres y apellidos
        """
        if not nombre or len(nombre.strip()) < 2:
            raise ValidationError(f"El {campo} debe tener al menos 2 caracteres")
        
        if len(nombre.strip()) > 100:
            raise ValidationError(f"El {campo} no puede exceder 100 caracteres")
        
        # Solo letras, espacios y algunos caracteres especiales
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre.strip()):
            raise ValidationError(f"El {campo} solo puede contener letras y espacios")
        
        return nombre.strip().title()
    
    @staticmethod
    def validar_rut_unico(rut):
        """
        Valida que el RUT no esté registrado
        """
        rut_data = RutValidationService.normalizar_rut(rut)
        
        # Verificar si ya existe
        if Usuario.objects.filter(rut=rut_data['numero'], dv=rut_data['dv']).exists():
            raise ValidationError("El RUT ya está registrado")
        
        return rut_data
    
    @staticmethod
    def validar_datos_usuario_completo(datos):
        """
        Valida todos los datos de un usuario
        """
        errores = {}
        datos_validados = {}
        
        try:
            # Validar nombre
            try:
                datos_validados['nombre'] = UsuarioValidationService.validar_nombre(
                    datos.get('nombre', ''), 'nombre'
                )
            except ValidationError as e:
                errores['nombre'] = str(e)
            
            # Validar apellido
            try:
                datos_validados['apellido'] = UsuarioValidationService.validar_nombre(
                    datos.get('apellido', ''), 'apellido'
                )
            except ValidationError as e:
                errores['apellido'] = str(e)
            
            # Validar email
            try:
                datos_validados['email'] = UsuarioValidationService.validar_email(
                    datos.get('email', '')
                )
            except ValidationError as e:
                errores['email'] = str(e)
            
            # Validar edad
            try:
                datos_validados['edad'] = UsuarioValidationService.validar_edad(
                    datos.get('edad')
                )
            except ValidationError as e:
                errores['edad'] = str(e)
            
            # Validar RUT
            try:
                rut_data = UsuarioValidationService.validar_rut_unico(
                    datos.get('rut', '')
                )
                datos_validados['rut'] = rut_data['numero']
                datos_validados['dv'] = rut_data['dv']
                datos_validados['rut_formateado'] = rut_data['rut_formateado']
            except ValidationError as e:
                errores['rut'] = str(e)
            
            # Si hay errores, lanzar excepción con todos los errores
            if errores:
                error_msg = "; ".join([f"{campo}: {error}" for campo, error in errores.items()])
                raise ValidationError(error_msg)
            
            logger.info(f"Datos de usuario validados exitosamente para RUT: {datos_validados.get('rut_formateado')}")
            return datos_validados
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error inesperado validando datos de usuario: {str(e)}")
            raise ValidationError("Error interno validando datos de usuario")
    
    @staticmethod
    def buscar_usuario_por_rut(rut):
        """
        Busca un usuario por RUT
        """
        try:
            rut_data = RutValidationService.normalizar_rut(rut)
            return Usuario.objects.get(rut=rut_data['numero'], dv=rut_data['dv'])
        except ValidationError:
            raise ValidationError("RUT inválido")
        except Usuario.DoesNotExist:
            raise ValidationError("Usuario no encontrado")
        except Exception as e:
            logger.error(f"Error buscando usuario por RUT: {str(e)}")
            raise ValidationError("Error interno buscando usuario")