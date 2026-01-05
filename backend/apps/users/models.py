"""
Modelo de Usuario personalizado con claves RSA.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.crypto_core.services import RSAService


class User(AbstractUser):
    """
    Usuario extendido con par de claves RSA.
    
    Cada usuario tiene su propio par de claves para
    cifrado asimétrico y firma digital.
    """
    
    # Claves RSA del usuario
    public_key = models.TextField(
        blank=True,
        help_text="Clave pública RSA en formato PEM"
    )
    private_key_encrypted = models.TextField(
        blank=True,
        help_text="Clave privada RSA cifrada"
    )
    key_size = models.IntegerField(
        default=2048,
        help_text="Tamaño de la clave RSA en bits"
    )
    
    # Timestamps
    keys_created_at = models.DateTimeField(
        null=True,
        blank=True
    )
    keys_rotated_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def generate_keys(self, key_size: int = 2048):
        """
        Genera un nuevo par de claves RSA para el usuario.
        """
        from django.utils import timezone
        
        private_pem, public_pem = RSAService.generate_key_pair(key_size)
        
        self.public_key = public_pem.decode('utf-8')
        # TODO: En producción, cifrar la clave privada con la contraseña del usuario
        self.private_key_encrypted = private_pem.decode('utf-8')
        self.key_size = key_size
        self.keys_created_at = timezone.now()
        self.save()
    
    def get_public_key_bytes(self) -> bytes:
        """Retorna la clave pública como bytes."""
        return self.public_key.encode('utf-8')
    
    def get_private_key_bytes(self) -> bytes:
        """Retorna la clave privada como bytes."""
        # TODO: Descifrar con la contraseña del usuario
        return self.private_key_encrypted.encode('utf-8')
    
    def has_keys(self) -> bool:
        """Verifica si el usuario tiene claves generadas."""
        return bool(self.public_key and self.private_key_encrypted)
