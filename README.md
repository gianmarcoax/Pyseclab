# P4 - Seguridad: PySec Lab

Laboratorio de seguridad con demostración de cifrado simétrico (AES) y asimétrico (RSA).

## 🚀 Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Estructura
```
├── backend/          # Django REST API
├── frontend/         # React + Vite
└── docs/             # Documentación
```

## Características
- Cifrado AES-256-CBC (simétrico)
- Cifrado RSA-2048 con firma digital (asimétrico)
- Visualización del proceso de cifrado
- Autenticación JWT
- Auditoría de operaciones

## Equipo
- Backend & Crypto: [Tu nombre]
- Pentesting: [Nombre de tu colega]
