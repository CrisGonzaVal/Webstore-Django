from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from ..models import Usuario, Cliente

class AuthService:
    @staticmethod
    def registrar_usuario(datos_usuario):
        """
        Registrar nuevo usuario con validaciones
        """
        # Validar datos
        if User.objects.filter(email=datos_usuario['email']).exists():
            raise ValidationError("El email ya está registrado")
        
        # Crear usuario Django
        user = User.objects.create_user(
            username=datos_usuario['email'],
            email=datos_usuario['email'],
            password=datos_usuario['password'],
            first_name=datos_usuario['nombre'],
            last_name=datos_usuario['apellido']
        )
        
        # Crear perfil de usuario personalizado
        usuario = Usuario.objects.create(
            nombre=datos_usuario['nombre'],
            apellido=datos_usuario['apellido'],
            email=datos_usuario['email'],
            rut=datos_usuario['rut'],
            edad=datos_usuario['edad']
        )
        
        Cliente.objects.create(usuario=usuario)
        
        return user, usuario
    
    @staticmethod
    def autenticar_usuario(email, password):
        """
        Autenticar usuario
        """
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            return user
        raise ValidationError("Credenciales inválidas")