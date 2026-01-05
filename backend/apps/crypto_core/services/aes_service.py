"""
Servicio de Cifrado AES-CBC
===========================

Implementación de cifrado simétrico AES usando la librería cryptography.
Soporta claves de 128, 192 y 256 bits con modo CBC.

Autor: Equipo P4 Seguridad
"""

import base64
import secrets
from typing import Tuple, Dict, Any

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class AESService:
    """
    Servicio de cifrado simétrico AES-CBC.
    
    Características:
    - Claves de 128, 192 o 256 bits
    - Modo CBC con IV aleatorio
    - Padding PKCS7
    """
    
    VALID_KEY_SIZES = [128, 192, 256]
    BLOCK_SIZE = 128  # AES block size in bits
    IV_SIZE = 16  # 128 bits
    
    @staticmethod
    def generate_key(key_size: int = 256) -> bytes:
        """
        Genera una clave AES criptográficamente segura.
        
        Args:
            key_size: Tamaño en bits (128, 192, 256)
            
        Returns:
            bytes: Clave generada
        """
        if key_size not in AESService.VALID_KEY_SIZES:
            raise ValueError(f"Key size must be one of {AESService.VALID_KEY_SIZES}")
        
        return secrets.token_bytes(key_size // 8)
    
    @staticmethod
    def generate_iv() -> bytes:
        """Genera un IV aleatorio."""
        return secrets.token_bytes(AESService.IV_SIZE)
    
    @staticmethod
    def encrypt(plaintext: str, key: bytes) -> Dict[str, Any]:
        """
        Cifra un mensaje con AES-CBC.
        
        Args:
            plaintext: Mensaje a cifrar
            key: Clave AES (16, 24 o 32 bytes)
            
        Returns:
            Dict con iv, ciphertext (ambos en base64), y metadatos
        """
        # Generar IV
        iv = AESService.generate_iv()
        
        # Convertir a bytes y aplicar padding
        plaintext_bytes = plaintext.encode('utf-8')
        padder = padding.PKCS7(AESService.BLOCK_SIZE).padder()
        padded_data = padder.update(plaintext_bytes) + padder.finalize()
        
        # Crear cipher y cifrar
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        return {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'algorithm': 'AES',
            'mode': 'CBC',
            'key_size': len(key) * 8,
            'padding': 'PKCS7'
        }
    
    @staticmethod
    def decrypt(ciphertext_b64: str, iv_b64: str, key: bytes) -> str:
        """
        Descifra un mensaje cifrado con AES-CBC.
        
        Args:
            ciphertext_b64: Texto cifrado en base64
            iv_b64: IV en base64
            key: Clave AES
            
        Returns:
            str: Mensaje descifrado
        """
        # Decodificar base64
        iv = base64.b64decode(iv_b64)
        ciphertext = base64.b64decode(ciphertext_b64)
        
        # Crear cipher y descifrar
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Quitar padding
        unpadder = padding.PKCS7(AESService.BLOCK_SIZE).unpadder()
        plaintext_bytes = unpadder.update(padded_data) + unpadder.finalize()
        
        return plaintext_bytes.decode('utf-8')
    
    @staticmethod
    def encrypt_with_steps(plaintext: str, key: bytes) -> Dict[str, Any]:
        """
        Cifra mostrando cada paso del proceso (para demostración).
        
        Returns:
            Dict con todos los pasos intermedios
        """
        steps = []
        
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
        
        # Paso 3: Aplicar padding PKCS7
        padder = padding.PKCS7(AESService.BLOCK_SIZE).padder()
        padded_data = padder.update(plaintext_bytes) + padder.finalize()
        padding_bytes = len(padded_data) - len(plaintext_bytes)
        steps.append({
            'step': 3,
            'name': 'Aplicar padding PKCS7',
            'data': padded_data.hex(),
            'type': 'hex',
            'padding_added': padding_bytes,
            'new_length': len(padded_data)
        })
        
        # Paso 4: Generar IV
        iv = AESService.generate_iv()
        steps.append({
            'step': 4,
            'name': 'Generar IV aleatorio',
            'data': iv.hex(),
            'type': 'hex',
            'length': len(iv)
        })
        
        # Paso 5: Mostrar clave (parcial por seguridad)
        steps.append({
            'step': 5,
            'name': 'Clave AES',
            'data': key[:4].hex() + '...' + key[-4:].hex(),
            'type': 'hex_partial',
            'key_size': len(key) * 8
        })
        
        # Paso 6: Cifrar con AES-CBC
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        steps.append({
            'step': 6,
            'name': 'Cifrar con AES-CBC',
            'data': ciphertext.hex(),
            'type': 'hex'
        })
        
        # Paso 7: Codificar en Base64
        result_b64 = base64.b64encode(iv + ciphertext).decode('utf-8')
        steps.append({
            'step': 7,
            'name': 'Codificar en Base64 (IV + Ciphertext)',
            'data': result_b64,
            'type': 'base64'
        })
        
        return {
            'steps': steps,
            'result': {
                'iv': base64.b64encode(iv).decode('utf-8'),
                'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
                'combined': result_b64
            },
            'algorithm': 'AES-CBC',
            'key_size': len(key) * 8
        }
    
    @staticmethod
    def key_to_base64(key: bytes) -> str:
        """Convierte clave a base64."""
        return base64.b64encode(key).decode('utf-8')
    
    @staticmethod
    def key_from_base64(key_b64: str) -> bytes:
        """Convierte base64 a clave."""
        return base64.b64decode(key_b64)
