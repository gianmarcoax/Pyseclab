"""
Servicio de Cifrado RSA con Firma Digital
==========================================

Implementación de cifrado asimétrico RSA usando la librería cryptography.
Incluye generación de claves, cifrado/descifrado y firma digital.

Autor: Equipo P4 Seguridad
"""

import base64
from typing import Dict, Any, Tuple, Optional

from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


class RSAService:
    """
    Servicio de cifrado asimétrico RSA.
    
    Características:
    - Claves de 2048, 3072 o 4096 bits
    - Cifrado con OAEP padding
    - Firma digital con PSS padding
    """
    
    VALID_KEY_SIZES = [2048, 3072, 4096]
    PUBLIC_EXPONENT = 65537
    
    @staticmethod
    def generate_key_pair(key_size: int = 2048) -> Tuple[bytes, bytes]:
        """
        Genera un par de claves RSA.
        
        Args:
            key_size: Tamaño en bits (2048, 3072, 4096)
            
        Returns:
            Tuple[bytes, bytes]: (private_key_pem, public_key_pem)
        """
        if key_size not in RSAService.VALID_KEY_SIZES:
            raise ValueError(f"Key size must be one of {RSAService.VALID_KEY_SIZES}")
        
        private_key = rsa.generate_private_key(
            public_exponent=RSAService.PUBLIC_EXPONENT,
            key_size=key_size,
            backend=default_backend()
        )
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    @staticmethod
    def _load_private_key(private_pem: bytes):
        """Carga una clave privada desde PEM."""
        return serialization.load_pem_private_key(
            private_pem,
            password=None,
            backend=default_backend()
        )
    
    @staticmethod
    def _load_public_key(public_pem: bytes):
        """Carga una clave pública desde PEM."""
        return serialization.load_pem_public_key(
            public_pem,
            backend=default_backend()
        )
    
    @staticmethod
    def _get_oaep_padding():
        """Retorna padding OAEP para cifrado."""
        return asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    
    @staticmethod
    def _get_pss_padding():
        """Retorna padding PSS para firma."""
        return asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        )
    
    @staticmethod
    def encrypt(plaintext: str, public_key_pem: bytes) -> Dict[str, Any]:
        """
        Cifra un mensaje con la clave pública RSA.
        
        Args:
            plaintext: Mensaje a cifrar
            public_key_pem: Clave pública en formato PEM
            
        Returns:
            Dict con ciphertext en base64 y metadatos
        """
        public_key = RSAService._load_public_key(public_key_pem)
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Verificar tamaño máximo
        key_size = public_key.key_size
        max_size = (key_size // 8) - 66  # OAEP overhead for SHA256
        
        if len(plaintext_bytes) > max_size:
            raise ValueError(
                f"Message too long ({len(plaintext_bytes)} bytes). "
                f"Max: {max_size} bytes for {key_size}-bit key."
            )
        
        ciphertext = public_key.encrypt(
            plaintext_bytes,
            RSAService._get_oaep_padding()
        )
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'algorithm': 'RSA',
            'padding': 'OAEP-SHA256',
            'key_size': key_size
        }
    
    @staticmethod
    def decrypt(ciphertext_b64: str, private_key_pem: bytes) -> str:
        """
        Descifra un mensaje con la clave privada RSA.
        
        Args:
            ciphertext_b64: Texto cifrado en base64
            private_key_pem: Clave privada en formato PEM
            
        Returns:
            str: Mensaje descifrado
        """
        private_key = RSAService._load_private_key(private_key_pem)
        ciphertext = base64.b64decode(ciphertext_b64)
        
        plaintext_bytes = private_key.decrypt(
            ciphertext,
            RSAService._get_oaep_padding()
        )
        
        return plaintext_bytes.decode('utf-8')
    
    @staticmethod
    def sign(message: str, private_key_pem: bytes) -> Dict[str, Any]:
        """
        Firma un mensaje con la clave privada.
        
        Args:
            message: Mensaje a firmar
            private_key_pem: Clave privada en formato PEM
            
        Returns:
            Dict con signature en base64 y metadatos
        """
        private_key = RSAService._load_private_key(private_key_pem)
        message_bytes = message.encode('utf-8')
        
        signature = private_key.sign(
            message_bytes,
            RSAService._get_pss_padding(),
            hashes.SHA256()
        )
        
        return {
            'signature': base64.b64encode(signature).decode('utf-8'),
            'algorithm': 'RSA-PSS',
            'hash': 'SHA256'
        }
    
    @staticmethod
    def verify(message: str, signature_b64: str, 
               public_key_pem: bytes) -> Dict[str, Any]:
        """
        Verifica una firma digital.
        
        Args:
            message: Mensaje original
            signature_b64: Firma en base64
            public_key_pem: Clave pública del firmante
            
        Returns:
            Dict con resultado de verificación
        """
        public_key = RSAService._load_public_key(public_key_pem)
        message_bytes = message.encode('utf-8')
        signature = base64.b64decode(signature_b64)
        
        try:
            public_key.verify(
                signature,
                message_bytes,
                RSAService._get_pss_padding(),
                hashes.SHA256()
            )
            return {'valid': True, 'message': 'Firma válida'}
        except InvalidSignature:
            return {'valid': False, 'message': 'Firma inválida'}
    
    @staticmethod
    def encrypt_with_steps(plaintext: str, public_key_pem: bytes) -> Dict[str, Any]:
        """
        Cifra mostrando cada paso del proceso (para demostración).
        """
        steps = []
        public_key = RSAService._load_public_key(public_key_pem)
        key_size = public_key.key_size
        
        # Paso 1: Mensaje original
        steps.append({
            'step': 1,
            'name': 'Mensaje original',
            'data': plaintext,
            'type': 'text'
        })
        
        # Paso 2: Convertir a bytes
        plaintext_bytes = plaintext.encode('utf-8')
        steps.append({
            'step': 2,
            'name': 'Convertir a bytes (UTF-8)',
            'data': plaintext_bytes.hex(),
            'type': 'hex',
            'length': len(plaintext_bytes)
        })
        
        # Paso 3: Mostrar clave pública (parcial)
        pub_pem_str = public_key_pem.decode('utf-8')
        steps.append({
            'step': 3,
            'name': 'Clave pública RSA',
            'data': pub_pem_str[:80] + '...',
            'type': 'pem_partial',
            'key_size': key_size
        })
        
        # Paso 4: Explicar OAEP padding
        steps.append({
            'step': 4,
            'name': 'Aplicar OAEP Padding',
            'data': 'OAEP (Optimal Asymmetric Encryption Padding) con SHA-256',
            'type': 'info',
            'details': 'Añade aleatoriedad al cifrado para mayor seguridad'
        })
        
        # Paso 5: Cifrar
        ciphertext = public_key.encrypt(
            plaintext_bytes,
            RSAService._get_oaep_padding()
        )
        steps.append({
            'step': 5,
            'name': 'Cifrar con RSA',
            'data': ciphertext.hex()[:64] + '...',
            'type': 'hex',
            'full_length': len(ciphertext)
        })
        
        # Paso 6: Codificar en Base64
        ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
        steps.append({
            'step': 6,
            'name': 'Codificar en Base64',
            'data': ciphertext_b64,
            'type': 'base64'
        })
        
        return {
            'steps': steps,
            'result': {
                'ciphertext': ciphertext_b64
            },
            'algorithm': f'RSA-{key_size}-OAEP'
        }
    
    @staticmethod
    def sign_with_steps(message: str, private_key_pem: bytes) -> Dict[str, Any]:
        """
        Firma mostrando cada paso del proceso (para demostración).
        """
        steps = []
        private_key = RSAService._load_private_key(private_key_pem)
        
        # Paso 1: Mensaje a firmar
        steps.append({
            'step': 1,
            'name': 'Mensaje a firmar',
            'data': message,
            'type': 'text'
        })
        
        # Paso 2: Calcular hash SHA-256
        message_bytes = message.encode('utf-8')
        import hashlib
        message_hash = hashlib.sha256(message_bytes).hexdigest()
        steps.append({
            'step': 2,
            'name': 'Calcular hash SHA-256',
            'data': message_hash,
            'type': 'hex'
        })
        
        # Paso 3: Aplicar PSS padding
        steps.append({
            'step': 3,
            'name': 'Aplicar PSS Padding',
            'data': 'PSS (Probabilistic Signature Scheme)',
            'type': 'info',
            'details': 'Añade sal aleatoria para firmas no determinísticas'
        })
        
        # Paso 4: Firmar con clave privada
        signature = private_key.sign(
            message_bytes,
            RSAService._get_pss_padding(),
            hashes.SHA256()
        )
        steps.append({
            'step': 4,
            'name': 'Firmar con clave privada',
            'data': signature.hex()[:64] + '...',
            'type': 'hex'
        })
        
        # Paso 5: Codificar en Base64
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        steps.append({
            'step': 5,
            'name': 'Codificar en Base64',
            'data': signature_b64,
            'type': 'base64'
        })
        
        return {
            'steps': steps,
            'result': {
                'signature': signature_b64,
                'message_hash': message_hash
            },
            'algorithm': 'RSA-PSS-SHA256'
        }
    
    @staticmethod
    def pem_to_base64(pem_data: bytes) -> str:
        """Convierte PEM a base64 simple."""
        return base64.b64encode(pem_data).decode('utf-8')
    
    @staticmethod
    def base64_to_pem(b64_data: str) -> bytes:
        """Convierte base64 a PEM."""
        return base64.b64decode(b64_data)
