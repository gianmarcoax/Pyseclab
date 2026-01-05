"""
Modelos para el sistema de mensajería cifrada.
"""
from django.db import models
from django.conf import settings


class Message(models.Model):
    """
    Mensaje cifrado entre usuarios.
    """
    
    ENCRYPTION_CHOICES = [
        ('AES', 'AES-256-CBC (Simétrico)'),
        ('RSA', 'RSA-2048 (Asimétrico)'),
        ('HYBRID', 'Híbrido (RSA + AES)'),
    ]
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    # Tipo de cifrado usado
    encryption_type = models.CharField(
        max_length=10,
        choices=ENCRYPTION_CHOICES,
        default='AES'
    )
    
    # Contenido cifrado
    ciphertext = models.TextField(
        help_text="Contenido del mensaje cifrado en base64"
    )
    
    # Metadatos de cifrado
    iv = models.CharField(
        max_length=64,
        blank=True,
        help_text="IV para AES en base64"
    )
    encrypted_key = models.TextField(
        blank=True,
        help_text="Clave AES cifrada con RSA (para híbrido)"
    )
    signature = models.TextField(
        blank=True,
        help_text="Firma digital del mensaje"
    )
    
    # Info adicional
    key_size = models.IntegerField(default=256)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        ordering = ['-created_at']
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
    
    def __str__(self):
        return f"{self.sender.username} -> {self.recipient.username} ({self.encryption_type})"


class SharedKey(models.Model):
    """
    Clave compartida entre dos usuarios para cifrado simétrico.
    """
    
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shared_keys_1'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shared_keys_2'
    )
    
    # La clave está cifrada con las claves públicas de ambos usuarios
    key_for_user1 = models.TextField(
        help_text="Clave cifrada con la clave pública del user1"
    )
    key_for_user2 = models.TextField(
        help_text="Clave cifrada con la clave pública del user2"
    )
    
    key_size = models.IntegerField(default=256)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'shared_keys'
        unique_together = ['user1', 'user2']
        verbose_name = 'Clave Compartida'
        verbose_name_plural = 'Claves Compartidas'
