"""
Serializadores para mensajería.
"""
from rest_framework import serializers
from .models import Message, SharedKey


class MessageSerializer(serializers.ModelSerializer):
    """Serializer para mensajes."""
    
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_username', 'recipient', 'recipient_username',
            'encryption_type', 'ciphertext', 'iv', 'encrypted_key', 'signature',
            'key_size', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at']


class SendMessageSerializer(serializers.Serializer):
    """Serializer para enviar un mensaje."""
    
    recipient_username = serializers.CharField()
    plaintext = serializers.CharField(max_length=10000)
    encryption_type = serializers.ChoiceField(
        choices=['AES', 'RSA', 'HYBRID'],
        default='AES'
    )
    # Opcional: clave AES compartida
    shared_key = serializers.CharField(required=False)


class MessageListSerializer(serializers.ModelSerializer):
    """Serializer para listado de mensajes."""
    
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    preview = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender_username', 'recipient_username',
            'encryption_type', 'is_read', 'created_at', 'preview'
        ]
    
    def get_preview(self, obj):
        return f"[Mensaje cifrado con {obj.encryption_type}]"


class SharedKeySerializer(serializers.ModelSerializer):
    """Serializer para claves compartidas."""
    
    class Meta:
        model = SharedKey
        fields = ['id', 'user1', 'user2', 'key_size', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']
