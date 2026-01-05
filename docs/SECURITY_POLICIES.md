# Políticas de Seguridad - CryptoMessenger

## 1. Algoritmos Implementados

### 1.1 Cifrado Simétrico: AES-256-CBC

**¿Por qué AES?**
- Estándar de cifrado aprobado por NIST
- Ampliamente auditado y probado
- Eficiente y rápido

**Configuración:**
| Parámetro | Valor |
|-----------|-------|
| Tamaño de clave | 128, 192 o 256 bits |
| Modo de operación | CBC (Cipher Block Chaining) |
| Padding | PKCS7 |
| IV | Aleatorio 128 bits (único por mensaje) |

**Uso de la librería `cryptography`:**
```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
```

### 1.2 Cifrado Asimétrico: RSA-2048 con OAEP

**¿Por qué RSA-OAEP?**
- OAEP es resistente a ataques de padding oracle
- Más seguro que PKCS1v15

**Configuración:**
| Parámetro | Valor |
|-----------|-------|
| Tamaño de clave | 2048, 3072 o 4096 bits |
| Padding (cifrado) | OAEP con SHA-256 |
| Padding (firma) | PSS con SHA-256 |

### 1.3 Firma Digital

Usamos RSA-PSS con SHA-256 para garantizar:
- **Integridad**: El mensaje no fue alterado
- **Autenticidad**: El mensaje proviene del remitente
- **No repudio**: El remitente no puede negar la firma

---

## 2. Gestión de Claves

### 2.1 Generación de Claves

- **Fuente de aleatoriedad**: `secrets.token_bytes()` (CSPRNG)
- Las claves se generan al momento del registro del usuario

### 2.2 Almacenamiento

| Tipo de clave | Almacenamiento |
|---------------|----------------|
| Claves AES | Generadas por sesión de mensaje |
| Claves RSA públicas | Base de datos (sin cifrar) |
| Claves RSA privadas | Base de datos (en producción deben cifrarse con contraseña del usuario) |

### 2.3 Rotación de Claves

**Recomendaciones:**
- Claves RSA: Rotar cada 1-2 años
- Claves AES de sesión: Una por mensaje (nunca reutilizar)

### 2.4 Distribución

- **AES**: La clave compartida debe transmitirse por canal seguro (fuera de banda)
- **RSA**: Las claves públicas se distribuyen vía API

---

## 3. Control de Acceso

### 3.1 Autenticación

- JWT (JSON Web Tokens) con expiración de 60 minutos
- Refresh tokens con expiración de 7 días
- Contraseñas hasheadas con Django (PBKDF2-SHA256)

### 3.2 Requisitos de Contraseña

- Mínimo 12 caracteres
- No puede ser similar al username/email
- No puede ser contraseña común
- No puede ser completamente numérica

### 3.3 Rate Limiting

| Tipo | Límite |
|------|--------|
| Usuarios anónimos | 20 requests/minuto |
| Usuarios autenticados | 100 requests/minuto |

---

## 4. Protección contra Ataques

### 4.1 Fuerza Bruta

- Bloqueo de cuenta después de 5 intentos fallidos
- Log de todos los intentos de login

### 4.2 Ataques de Temporización

- Uso de `hmac.compare_digest()` para comparaciones de claves
- Tiempos de respuesta constantes

### 4.3 Inyección SQL

- Django ORM previene inyecciones automáticamente
- No se usan queries raw

### 4.4 XSS/CSRF

- Django CSRF protection habilitado
- CORS configurado solo para frontend autorizado

---

## 5. Auditoría

Se registran los siguientes eventos:
- `LOGIN` / `LOGIN_FAILED` / `LOGOUT`
- `KEY_GENERATE` / `KEY_ROTATE`
- `ENCRYPT` / `DECRYPT`
- `SIGN` / `VERIFY`
- `MESSAGE_SEND` / `MESSAGE_READ`

Alertas automáticas para:
- Múltiples intentos de login fallidos (fuerza bruta)
- Actividad sospechosa

---

## 6. Configuración de Seguridad (Producción)

```python
# settings.py - Producción
DEBUG = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```
