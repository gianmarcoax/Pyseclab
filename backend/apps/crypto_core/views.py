"""
Views para operaciones criptográficas de demostración.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .services import AESService, RSAService
from .serializers import (
    AESEncryptSerializer, AESDecryptSerializer,
    RSAEncryptSerializer, RSADecryptSerializer,
    RSASignSerializer, RSAVerifySerializer,
    GenerateKeySerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def generate_keys(request):
    """
    Genera claves criptográficas.
    
    POST /api/crypto/keys/generate/
    {
        "algorithm": "AES" | "RSA",
        "key_size": 256 | 2048
    }
    """
    serializer = GenerateKeySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    algo = serializer.validated_data['algorithm']
    key_size = serializer.validated_data['key_size']
    
    try:
        if algo == 'AES':
            key = AESService.generate_key(key_size)
            return Response({
                'algorithm': 'AES',
                'key_size': key_size,
                'key': AESService.key_to_base64(key)
            })
        else:
            private_pem, public_pem = RSAService.generate_key_pair(key_size)
            return Response({
                'algorithm': 'RSA',
                'key_size': key_size,
                'private_key': private_pem.decode('utf-8'),
                'public_key': public_pem.decode('utf-8')
            })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def aes_encrypt(request):
    """
    Cifra con AES-CBC mostrando pasos.
    
    POST /api/crypto/aes/encrypt/
    """
    serializer = AESEncryptSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    plaintext = serializer.validated_data['plaintext']
    key_size = serializer.validated_data['key_size']
    key_b64 = serializer.validated_data.get('key')
    
    try:
        if key_b64:
            key = AESService.key_from_base64(key_b64)
        else:
            key = AESService.generate_key(key_size)
        
        result = AESService.encrypt_with_steps(plaintext, key)
        result['key'] = AESService.key_to_base64(key)
        
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def aes_decrypt(request):
    """
    Descifra con AES-CBC.
    
    POST /api/crypto/aes/decrypt/
    """
    serializer = AESDecryptSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        key = AESService.key_from_base64(serializer.validated_data['key'])
        plaintext = AESService.decrypt(
            serializer.validated_data['ciphertext'],
            serializer.validated_data['iv'],
            key
        )
        
        return Response({
            'plaintext': plaintext,
            'algorithm': 'AES-CBC'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def rsa_encrypt(request):
    """
    Cifra con RSA mostrando pasos.
    
    POST /api/crypto/rsa/encrypt/
    """
    serializer = RSAEncryptSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        public_key = serializer.validated_data['public_key']
        
        # Handle both PEM and base64 formats
        if not public_key.startswith('-----BEGIN'):
            public_key = RSAService.base64_to_pem(public_key)
        else:
            public_key = public_key.encode('utf-8')
        
        result = RSAService.encrypt_with_steps(
            serializer.validated_data['plaintext'],
            public_key
        )
        
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def rsa_decrypt(request):
    """
    Descifra con RSA.
    
    POST /api/crypto/rsa/decrypt/
    """
    serializer = RSADecryptSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        private_key = serializer.validated_data['private_key']
        
        if not private_key.startswith('-----BEGIN'):
            private_key = RSAService.base64_to_pem(private_key)
        else:
            private_key = private_key.encode('utf-8')
        
        plaintext = RSAService.decrypt(
            serializer.validated_data['ciphertext'],
            private_key
        )
        
        return Response({
            'plaintext': plaintext,
            'algorithm': 'RSA-OAEP'
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def rsa_sign(request):
    """
    Firma un mensaje con RSA mostrando pasos.
    
    POST /api/crypto/rsa/sign/
    """
    serializer = RSASignSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        private_key = serializer.validated_data['private_key']
        
        if not private_key.startswith('-----BEGIN'):
            private_key = RSAService.base64_to_pem(private_key)
        else:
            private_key = private_key.encode('utf-8')
        
        result = RSAService.sign_with_steps(
            serializer.validated_data['message'],
            private_key
        )
        
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def rsa_verify(request):
    """
    Verifica una firma digital.
    
    POST /api/crypto/rsa/verify/
    """
    serializer = RSAVerifySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        public_key = serializer.validated_data['public_key']
        
        if not public_key.startswith('-----BEGIN'):
            public_key = RSAService.base64_to_pem(public_key)
        else:
            public_key = public_key.encode('utf-8')
        
        result = RSAService.verify(
            serializer.validated_data['message'],
            serializer.validated_data['signature'],
            public_key
        )
        
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
