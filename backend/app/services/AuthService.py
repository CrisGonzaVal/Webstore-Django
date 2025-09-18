from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from ..models import Usuario, Cliente, TipoUsuario
from .UsuarioValidationService import UsuarioValidationService
from .RutValidationService import RutValidationService
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def registrar_usuario(datos_usuario):
        """
        Registrar nuevo usuario con validaciones completas
        """
        try:
            # Validar todos los datos usando el servicio de validación
            datos_validados = UsuarioValidationService.validar_datos_usuario_completo(datos_usuario)
            
            # Validar contraseña
            if not datos_usuario.get('password') or len(datos_usuario['password']) < 8:
                raise ValidationError("La contraseña debe tener al menos 8 caracteres")
            
            # Crear usuario Django
            user = User.objects.create_user(
                username=datos_validados['email'],
                email=datos_validados['email'],
                password=datos_usuario['password'],
                first_name=datos_validados['nombre'],
                last_name=datos_validados['apellido']
            )
            
            # Obtener o crear tipo de usuario por defecto (Cliente)
            tipo_cliente, created = TipoUsuario.objects.get_or_create(
                nombre='Cliente',
                defaults={'nombre': 'Cliente'}
            )
            
            # Crear perfil de usuario personalizado
            usuario = Usuario.objects.create(
                nombre=datos_validados['nombre'],
                apellido=datos_validados['apellido'],
                email=datos_validados['email'],
                rut=datos_validados['rut'],
                dv=datos_validados['dv'],
                edad=datos_validados['edad'],
                tipo_usuario=tipo_cliente
            )
            
            # Crear cliente
            Cliente.objects.create(usuario=usuario)
            
            logger.info(f"Usuario registrado exitosamente: {datos_validados['rut_formateado']}")
            
            return {
                'success': True,
                'user': user,
                'usuario': usuario,
                'rut_formateado': datos_validados['rut_formateado'],
                'message': 'Usuario registrado exitosamente'
            }
            
        except ValidationError as e:
            logger.error(f"Error de validación en registro: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error inesperado en registro: {str(e)}")
            raise ValidationError("Error interno al registrar usuario")
    
    @staticmethod
    def autenticar_usuario(email_o_rut, password):
        """
        Autenticar usuario por email o RUT
        """
        try:
            user = None
            
            # Intentar primero por email
            if '@' in email_o_rut:
                user = authenticate(username=email_o_rut, password=password)
            else:
                # Intentar por RUT
                try:
                    usuario = UsuarioValidationService.buscar_usuario_por_rut(email_o_rut)
                    user = authenticate(username=usuario.email, password=password)
                except ValidationError:
                    # Si el RUT no es válido, intentar como email de todas formas
                    user = authenticate(username=email_o_rut, password=password)
            
            if user and user.is_active:
                logger.info(f"Usuario autenticado: {user.email}")
                return user
            
            logger.warning(f"Intento de autenticación fallido para: {email_o_rut}")
            raise ValidationError("Credenciales inválidas")
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error inesperado en autenticación: {str(e)}")
            raise ValidationError("Error interno de autenticación")
    
    @staticmethod
    def buscar_usuario_por_rut(rut):
        """
        Buscar usuario por RUT (delegando al servicio de validación)
        """
        return UsuarioValidationService.buscar_usuario_por_rut(rut)