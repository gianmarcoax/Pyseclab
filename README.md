# 🔐 PySec Lab

Laboratorio de seguridad con demostración de cifrado simétrico (AES) y asimétrico (RSA).

## 📋 Requisitos Previos

- **Python** 3.10 o superior
- **Node.js** 18 o superior
- **Git**

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/gianmarcoax/Pyseclab.git
cd Pyseclab
```

### 2. Configurar el Backend (Django)

```bash
# Entrar a la carpeta del backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de configuración
copy ..\env.example .env   # Windows
# cp ../.env.example .env  # Linux/Mac

# Aplicar migraciones
python manage.py migrate

# (Opcional) Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

El backend estará disponible en: `http://localhost:8000`

### 3. Configurar el Frontend (React)

Abre una **nueva terminal**:

```bash
# Entrar a la carpeta del frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 🎮 Uso

1. Abre `http://localhost:5173` en tu navegador
2. Crea una cuenta en "Regístrate"
3. Inicia sesión
4. Explora:
   - **Demo de Cifrado**: Visualiza AES y RSA paso a paso
   - **Nuevo Mensaje**: Envía mensajes cifrados
   - **Mensajes**: Ve y descifra mensajes recibidos

## 📁 Estructura del Proyecto

```
Pyseclab/
├── backend/                 # Django REST API
│   ├── apps/
│   │   ├── crypto_core/     # Servicios AES y RSA
│   │   ├── users/           # Autenticación JWT
│   │   ├── messaging/       # Mensajes cifrados
│   │   └── audit/           # Logs de seguridad
│   ├── config/              # Configuración Django
│   └── requirements.txt
├── frontend/                # React + Vite
│   └── src/
│       ├── pages/           # Páginas de la app
│       ├── services/        # Llamadas a la API
│       └── components/      # Componentes UI
└── docs/                    # Documentación
    ├── SECURITY_POLICIES.md
    └── PENTESTING_GUIDE.md
```

## 🔒 Características de Seguridad

| Característica | Implementación |
|----------------|----------------|
| Cifrado Simétrico | AES-256-CBC con PKCS7 |
| Cifrado Asimétrico | RSA-2048 con OAEP |
| Firma Digital | RSA-PSS con SHA-256 |
| Autenticación | JWT (JSON Web Tokens) |
| Contraseñas | PBKDF2-SHA256 (mín. 12 chars) |

## 👥 Equipo

- **Backend & Crypto**: Gianmarco
- **Pentesting**: [Colaborador]

## 📝 Licencia

Proyecto académico - Universidad 2026
