"""
Serializadores para operaciones criptográficas.
"""
from rest_framework import serializers


class AESEncryptSerializer(serializers.Serializer):
    """Serializer para cifrado AES."""
    plaintext = serializers.CharField(max_length=10000)
    key_size = serializers.ChoiceField(choices=[128, 192, 256], default=256)
    key = serializers.CharField(required=False, help_text="Clave en base64 (opcional)")


class AESDecryptSerializer(serializers.Serializer):
    """Serializer para descifrado AES."""
    ciphertext = serializers.CharField()
    iv = serializers.CharField()
    key = serializers.CharField(help_text="Clave en base64")


class RSAEncryptSerializer(serializers.Serializer):
    """Serializer para cifrado RSA."""
    plaintext = serializers.CharField(max_length=500)
    public_key = serializers.CharField(help_text="Clave pública en base64 o PEM")


class RSADecryptSerializer(serializers.Serializer):
    """Serializer para descifrado RSA."""
    ciphertext = serializers.CharField()
    private_key = serializers.CharField(help_text="Clave privada en base64 o PEM")


class RSASignSerializer(serializers.Serializer):
    """Serializer para firma digital."""
    message = serializers.CharField(max_length=10000)
    private_key = serializers.CharField(help_text="Clave privada en base64 o PEM")


class RSAVerifySerializer(serializers.Serializer):
    """Serializer para verificación de firma."""
    message = serializers.CharField(max_length=10000)
    signature = serializers.CharField()
    public_key = serializers.CharField(help_text="Clave pública en base64 o PEM")


class GenerateKeySerializer(serializers.Serializer):
    """Serializer para generación de claves."""
    algorithm = serializers.ChoiceField(choices=['AES', 'RSA'])
    key_size = serializers.IntegerField()
    
    def validate(self, data):
        algo = data['algorithm']
        size = data['key_size']
        
        if algo == 'AES' and size not in [128, 192, 256]:
            raise serializers.ValidationError("AES key size must be 128, 192, or 256")
        if algo == 'RSA' and size not in [2048, 3072, 4096]:
            raise serializers.ValidationError("RSA key size must be 2048, 3072, or 4096")
        
        return data
