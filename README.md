# Rentcar — Guía rápida para colaboradores



Resumen
- Proyecto Django para gestionar vehículos y reservas.
- Configuración por defecto: PostgreSQL (variables en `.env`). También es posible usar SQLite para desarrollo.

Requisitos mínimos
- Python 3.10+
- Git
-  PostgreSQL

1) Clonar el repositorio

```cmd
git clone <repo-url>
cd Rentcar
```

2) Crear y activar un entorno virtual (Windows - cmd)

```cmd
python -m venv .venv
.venv\Scripts\activate
```

3) Instalar dependencias

```cmd
pip install -r requirements.txt
```

4) Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto (NO subirlo al repositorio). Ejemplo mínimo:

```env
# Django
SECRET_KEY=replace_me_with_a_secure_value
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# PostgreSQL (opcional)
DB_NAME=rentcar_db
DB_USER=rentcar_user
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5432
```

5) Migraciones y superusuario

```cmd
python manage.py migrate
python manage.py createsuperuser
```

6) Cargar datos de ejemplo (opcional)

```cmd
python scripts\create_samples.py
```

7) Ejecutar el servidor en desarrollo

```cmd
python manage.py runserver
```

Estructura del proyecto (resumen para colaboradores)

- `manage.py` — comandos de Django.
- `rentcar/` — configuración del proyecto (`settings.py`, `urls.py`, `wsgi.py`).
- `rentals/` — app principal: modelos, vistas, formularios, tests y admin.
  - `rentals/models.py` — `Vehicle`, `Reservation`.
  - `rentals/forms.py` — formularios: registro, login y reserva.
  - `rentals/views.py` — vistas públicas y administrativas.
  - `rentals/urls.py` — rutas de la app (namespace `rentals`).
- `templates/` — plantillas HTML (incluye `templates/rentals/`).
- `static/` — CSS, imágenes y otros assets.
- `scripts/` — utilidades (por ejemplo `create_samples.py`).

Dependencias y notas sobre `requirements.txt`

- `requirements.txt` contiene las librerías necesarias actualmente:
  - `Django>=4.2`
  - `psycopg2-binary` (si usas PostgreSQL)
  - `python-dotenv` (lee `.env`)

- Si añades subida de imágenes con `ImageField`, agrega `Pillow`.

Comandos útiles

- Ejecutar la shell de Django:

```cmd
python manage.py shell
```

```cmd
python manage.py test
```

Buenas prácticas para commits y PRs

1. Crear una rama por feature: `git checkout -b feat/mi-cambio`.
2. Hacer commits pequeños y con mensajes descriptivos.
3. Abrir pull request hacia `main` y pedir revisión.

Checklist antes de PR

- Ejecutaste `migrate` y probaste los flujos principales.
- No subiste `.env` ni datos sensibles.
- Añadiste tests cuando corresponde.


