"""
Views para autenticación y gestión de usuarios.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import (
    UserSerializer, RegisterSerializer, 
    CustomTokenObtainPairSerializer,
    PublicKeySerializer, GenerateUserKeysSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Vista de login con JWT personalizado."""
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registra un nuevo usuario.
    
    POST /api/auth/register/
    {
        "username": "usuario",
        "email": "email@example.com",
        "password": "ContraseñaSegura123!",
        "password_confirm": "ContraseñaSegura123!",
        "generate_keys": true,
        "key_size": 2048
    }
    """
    serializer = RegisterSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = serializer.save()
    
    response_data = {
        'message': 'Usuario registrado exitosamente',
        'user': UserSerializer(user).data
    }
    
    if user.has_keys():
        response_data['keys_generated'] = True
        response_data['public_key'] = user.public_key
    
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """
    Obtiene información del usuario actual.
    
    GET /api/auth/me/
    """
    return Response(UserSerializer(request.user).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_keys(request):
    """
    Obtiene las claves del usuario actual.
    
    GET /api/auth/me/keys/
    """
    user = request.user
    
    if not user.has_keys():
        return Response(
            {'error': 'No tienes claves generadas'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response({
        'public_key': user.public_key,
        'private_key': user.private_key_encrypted,  # Solo para demo
        'key_size': user.key_size,
        'created_at': user.keys_created_at
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_my_keys(request):
    """
    Genera nuevas claves para el usuario actual.
    
    POST /api/auth/me/keys/generate/
    """
    serializer = GenerateUserKeysSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    key_size = serializer.validated_data['key_size']
    request.user.generate_keys(key_size)
    
    return Response({
        'message': 'Claves generadas exitosamente',
        'public_key': request.user.public_key,
        'key_size': key_size
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def get_public_key(request):
    """
    Obtiene la clave pública de un usuario por username.
    
    POST /api/auth/users/public-key/
    """
    serializer = PublicKeySerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(username=serializer.validated_data['username'])
        
        if not user.has_keys():
            return Response(
                {'error': 'El usuario no tiene claves públicas'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'username': user.username,
            'public_key': user.public_key,
            'key_size': user.key_size
        })
        
    except User.DoesNotExist:
        return Response(
            {'error': 'Usuario no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    """
    Lista usuarios con sus claves públicas.
    
    GET /api/auth/users/
    """
    users = User.objects.exclude(id=request.user.id).filter(public_key__isnull=False)
    
    return Response({
        'users': [
            {
                'id': u.id,
                'username': u.username,
                'has_keys': u.has_keys()
            }
            for u in users
        ]
    })
