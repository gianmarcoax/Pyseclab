# Guía de Despliegue en PythonAnywhere

## Paso 1: Crear cuenta en PythonAnywhere

1. Ve a [pythonanywhere.com](https://www.pythonanywhere.com)
2. Crea una cuenta gratuita (plan "Beginner")
3. Tu URL será: `TU_USUARIO.pythonanywhere.com`

---

## Paso 2: Clonar el repositorio

En PythonAnywhere, abre una **Bash console** y ejecuta:

```bash
git clone https://github.com/gianmarcoax/Pyseclab.git
cd Pyseclab
```

---

## Paso 3: Crear entorno virtual

```bash
mkvirtualenv --python=/usr/bin/python3.10 pyseclab
pip install -r backend/requirements.txt
```

---

## Paso 4: Configurar variables de entorno

Crea el archivo `.env` en la carpeta `backend`:

```bash
cd ~/Pyseclab/backend
nano .env
```

Contenido:
```
DEBUG=False
SECRET_KEY=tu-clave-secreta-super-larga-aqui-cambiar
ALLOWED_HOSTS=TU_USUARIO.pythonanywhere.com
```

Guarda con `Ctrl+O`, `Enter`, `Ctrl+X`

---

## Paso 5: Configurar la base de datos

```bash
cd ~/Pyseclab/backend
python manage.py migrate
python manage.py createsuperuser
```

---

## Paso 6: Build del Frontend

**Opción A - En tu máquina local:**
```bash
cd frontend
npm run build
```
Luego sube la carpeta `dist/` a PythonAnywhere.

**Opción B - Frontend en Vercel/Netlify (recomendado para plan gratuito)**

---

## Paso 7: Crear Web App en PythonAnywhere

1. Ve a la pestaña **"Web"**
2. Click en **"Add a new web app"**
3. Selecciona **"Manual configuration"**
4. Selecciona **Python 3.10**

---

## Paso 8: Configurar WSGI

Click en el enlace del archivo WSGI y reemplaza TODO el contenido con:

```python
import os
import sys

# Añadir el proyecto al path
path = '/home/TU_USUARIO/Pyseclab/backend'
if path not in sys.path:
    sys.path.append(path)

# Configurar Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Cargar la aplicación
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**IMPORTANTE**: Reemplaza `TU_USUARIO` con tu nombre de usuario de PythonAnywhere.

---

## Paso 9: Configurar Virtualenv

En la pestaña Web, busca "Virtualenv" y pon:
```
/home/TU_USUARIO/.virtualenvs/pyseclab
```

---

## Paso 10: Archivos Estáticos

En la sección "Static files" de la pestaña Web:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/TU_USUARIO/Pyseclab/backend/static` |

Luego en la consola:
```bash
cd ~/Pyseclab/backend
python manage.py collectstatic
```

---

## Paso 11: Reload

Click en el botón verde **"Reload"** en la pestaña Web.

---

## Verificar

Visita `https://TU_USUARIO.pythonanywhere.com/api/` para verificar que la API funciona.

---

## Notas Importantes

- El plan gratuito solo permite **una** web app
- El plan gratuito tiene whitelist de dominios externos
- Para el frontend completo, considera **Vercel** o **Netlify** (gratis)
