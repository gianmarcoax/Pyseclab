"""
Serializadores para autenticación y usuarios.
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico de usuario."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'public_key', 'key_size', 'keys_created_at']
        read_only_fields = ['id', 'public_key', 'key_size', 'keys_created_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer para registro de usuarios."""
    
    password = serializers.CharField(
        write_only=True,
        min_length=12,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)
    generate_keys = serializers.BooleanField(default=True)
    key_size = serializers.ChoiceField(
        choices=[2048, 3072, 4096],
        default=2048
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'generate_keys', 'key_size']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden'
            })
        return data
    
    def create(self, validated_data):
        generate_keys = validated_data.pop('generate_keys', True)
        key_size = validated_data.pop('key_size', 2048)
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        if generate_keys:
            user.generate_keys(key_size)
        
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer JWT personalizado con info adicional."""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Agregar claims personalizados
        token['username'] = user.username
        token['has_keys'] = user.has_keys()
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Agregar info del usuario en la respuesta
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'has_keys': self.user.has_keys(),
            'public_key': self.user.public_key if self.user.has_keys() else None
        }
        
        return data


class PublicKeySerializer(serializers.Serializer):
    """Serializer para obtener clave pública de un usuario."""
    username = serializers.CharField()


class GenerateUserKeysSerializer(serializers.Serializer):
    """Serializer para generar claves de usuario."""
    key_size = serializers.ChoiceField(
        choices=[2048, 3072, 4096],
        default=2048
    )
