"""
Views para mensajería cifrada.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from apps.users.models import User
from apps.crypto_core.services import AESService, RSAService
from .models import Message
from .serializers import (
    MessageSerializer, SendMessageSerializer, MessageListSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_messages(request):
    """
    Lista mensajes del usuario (enviados y recibidos).
    
    GET /api/messages/
    """
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).select_related('sender', 'recipient')
    
    return Response({
        'messages': MessageListSerializer(messages, many=True).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inbox(request):
    """
    Mensajes recibidos.
    
    GET /api/messages/inbox/
    """
    messages = Message.objects.filter(
        recipient=request.user
    ).select_related('sender')
    
    return Response({
        'messages': MessageListSerializer(messages, many=True).data,
        'unread_count': messages.filter(is_read=False).count()
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sent(request):
    """
    Mensajes enviados.
    
    GET /api/messages/sent/
    """
    messages = Message.objects.filter(
        sender=request.user
    ).select_related('recipient')
    
    return Response({
        'messages': MessageListSerializer(messages, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    Envía un mensaje cifrado.
    
    POST /api/messages/send/
    """
    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Buscar destinatario
    try:
        recipient = User.objects.get(username=data['recipient_username'])
    except User.DoesNotExist:
        return Response(
            {'error': 'Destinatario no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    encryption_type = data['encryption_type']
    plaintext = data['plaintext']
    encryption_steps = []
    
    try:
        if encryption_type == 'AES':
            # Cifrado simétrico
            key = AESService.generate_key(256)
            result = AESService.encrypt_with_steps(plaintext, key)
            
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                encryption_type='AES',
                ciphertext=result['result']['ciphertext'],
                iv=result['result']['iv'],
                key_size=256
            )
            
            encryption_steps = result['steps']
            response_data = {
                'message': MessageSerializer(message).data,
                'encryption_steps': encryption_steps,
                'shared_key': AESService.key_to_base64(key),
                'note': 'Comparte esta clave de forma segura con el destinatario'
            }
            
        elif encryption_type == 'RSA':
            # Cifrado asimétrico
            if not recipient.has_keys():
                return Response(
                    {'error': 'El destinatario no tiene claves públicas'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Cifrar con clave pública del destinatario
            result = RSAService.encrypt_with_steps(
                plaintext,
                recipient.get_public_key_bytes()
            )
            
            # Firmar con clave privada del remitente
            signature_result = None
            signature = ''
            if request.user.has_keys():
                signature_result = RSAService.sign_with_steps(
                    plaintext,
                    request.user.get_private_key_bytes()
                )
                signature = signature_result['result']['signature']
            
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                encryption_type='RSA',
                ciphertext=result['result']['ciphertext'],
                signature=signature,
                key_size=recipient.key_size
            )
            
            response_data = {
                'message': MessageSerializer(message).data,
                'encryption_steps': result['steps'],
                'signature_steps': signature_result['steps'] if signature_result else None
            }
            
        else:  # HYBRID
            # Cifrado híbrido: AES para datos, RSA para clave
            if not recipient.has_keys():
                return Response(
                    {'error': 'El destinatario no tiene claves públicas'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generar clave AES
            aes_key = AESService.generate_key(256)
            
            # Cifrar mensaje con AES
            aes_result = AESService.encrypt_with_steps(plaintext, aes_key)
            
            # Cifrar clave AES con RSA
            encrypted_key = RSAService.encrypt(
                AESService.key_to_base64(aes_key),
                recipient.get_public_key_bytes()
            )
            
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                encryption_type='HYBRID',
                ciphertext=aes_result['result']['ciphertext'],
                iv=aes_result['result']['iv'],
                encrypted_key=encrypted_key['ciphertext'],
                key_size=256
            )
            
            response_data = {
                'message': MessageSerializer(message).data,
                'encryption_steps': aes_result['steps'],
                'key_encryption': 'Clave AES cifrada con RSA'
            }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_message(request, message_id):
    """
    Obtiene y descifra un mensaje.
    
    GET /api/messages/<id>/
    """
    try:
        message = Message.objects.get(
            Q(id=message_id),
            Q(sender=request.user) | Q(recipient=request.user)
        )
    except Message.DoesNotExist:
        return Response(
            {'error': 'Mensaje no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Marcar como leído
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()
    
    response_data = {
        'message': MessageSerializer(message).data,
        'can_decrypt': False,
        'plaintext': None
    }
    
    # Info para descifrado
    if message.encryption_type == 'AES':
        response_data['decrypt_info'] = {
            'type': 'AES',
            'requires': 'shared_key',
            'note': 'Necesitas la clave compartida para descifrar'
        }
    elif message.encryption_type == 'RSA':
        if message.recipient == request.user:
            response_data['can_decrypt'] = True
            response_data['decrypt_info'] = {
                'type': 'RSA',
                'note': 'Puedes descifrar con tu clave privada'
            }
    elif message.encryption_type == 'HYBRID':
        if message.recipient == request.user:
            response_data['can_decrypt'] = True
            response_data['decrypt_info'] = {
                'type': 'HYBRID',
                'note': 'Primero se descifra la clave AES con RSA'
            }
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrypt_message(request, message_id):
    """
    Descifra un mensaje.
    
    POST /api/messages/<id>/decrypt/
    """
    try:
        message = Message.objects.get(id=message_id, recipient=request.user)
    except Message.DoesNotExist:
        return Response(
            {'error': 'Mensaje no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        if message.encryption_type == 'AES':
            # Necesita clave compartida
            shared_key = request.data.get('shared_key')
            if not shared_key:
                return Response(
                    {'error': 'Se requiere shared_key'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            key = AESService.key_from_base64(shared_key)
            plaintext = AESService.decrypt(message.ciphertext, message.iv, key)
            
        elif message.encryption_type == 'RSA':
            # Descifrar con clave privada del destinatario
            plaintext = RSAService.decrypt(
                message.ciphertext,
                request.user.get_private_key_bytes()
            )
            
            # Verificar firma si existe
            signature_valid = None
            if message.signature:
                try:
                    sender = message.sender
                    if sender.has_keys():
                        result = RSAService.verify(
                            plaintext,
                            message.signature,
                            sender.get_public_key_bytes()
                        )
                        signature_valid = result['valid']
                except:
                    signature_valid = False
                    
        elif message.encryption_type == 'HYBRID':
            # Descifrar clave AES con RSA
            aes_key_b64 = RSAService.decrypt(
                message.encrypted_key,
                request.user.get_private_key_bytes()
            )
            aes_key = AESService.key_from_base64(aes_key_b64)
            
            # Descifrar mensaje con AES
            plaintext = AESService.decrypt(message.ciphertext, message.iv, aes_key)
            
        return Response({
            'plaintext': plaintext,
            'encryption_type': message.encryption_type,
            'signature_valid': signature_valid if message.encryption_type == 'RSA' else None
        })
        
    except Exception as e:
        return Response(
            {'error': f'Error al descifrar: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
