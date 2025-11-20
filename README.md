# Rentcar — Guía rápida (Windows)

Proyecto Django para gestionar vehículos y reservas, con generación de comprobantes en PDF.

## Requisitos
- Python 3.10+
- Git
- PostgreSQL (recomendado; puedes usar SQLite para desarrollo si lo prefieres)

## 1) Clonar

```cmd
git clone <repo-url>
cd Rentcar-Proyecto
```

## 2) Crear venv e instalar dependencias

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Si tienes problemas con permisos o múltiples Pythons, usa el ejecutable de la venv explícitamente:

```cmd
"%CD%\.venv\Scripts\pip.exe" install -r requirements.txt
```

## 3) Variables de entorno
Crea un archivo `.env` en la raíz del proyecto (no lo subas al repo). Ejemplo mínimo:

```env
# Django
SECRET_KEY=replace_me_with_a_secure_value
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Base de datos (PostgreSQL)
DB_NAME=rentcar_db
DB_USER=rentcar_user
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5432
```

Zona horaria (settings.py):
- Ajustada a `America/Asuncion`. Cambia este valor si tu equipo está en otra zona.

## 4) Migraciones y superusuario

```cmd
"%CD%\.venv\Scripts\python.exe" manage.py migrate
"%CD%\.venv\Scripts\python.exe" manage.py createsuperuser
```

## 5) Datos de ejemplo (opcional)

```cmd
"%CD%\.venv\Scripts\python.exe" scripts\create_samples.py
```

## 6) Ejecutar el servidor (usa SIEMPRE la venv)

Para evitar el error de librerías (por ejemplo, `No module named 'xhtml2pdf'`), arranca con el Python de la venv:

```cmd
"%CD%\.venv\Scripts\python.exe" manage.py runserver
```

## 7) Comprobantes (factura)
- Al confirmar una renta, se descarga automáticamente el PDF del comprobante.
- También puedes:
  - Ver el comprobante en HTML: `/reservations/<id>/invoice/`
  - Descargar el PDF: `/reservations/<id>/invoice/download/`
- En “Mis Rentas” y en el admin de Django, hay botones de “Ver comprobante” y “Descargar PDF”.

## Estructura
- `manage.py` — comandos de Django.
- `rentcar/` — settings, urls, wsgi.
- `rentals/` — app principal (modelos, vistas, formularios, admin).
- `templates/` — plantillas HTML.
- `static/` — CSS, imágenes y assets.
- `scripts/` — utilidades.

## Dependencias clave
- `Django>=4.2`
- `python-dotenv`
- `psycopg2-binary` (si usas PostgreSQL)
- `Pillow`
- `xhtml2pdf` (PDF; incluye `reportlab`, `pypdf` y otras)

En Linux/macOS, puede requerir librerías del sistema (cairo/pango) para PDF. En Windows suele funcionar sin pasos extra.

## Comandos útiles

```cmd
"%CD%\.venv\Scripts\python.exe" manage.py shell
"%CD%\.venv\Scripts\python.exe" manage.py test
```

## Flujo de trabajo
1. Crea una rama por feature: `git checkout -b feat/mi-cambio`.
2. Commits pequeños y descriptivos.
3. Abre PR y solicita revisión.

Checklist antes del PR:
- Ejecutaste migraciones y probaste los flujos.
- No subiste `.env` ni secretos.
- Agregaste tests cuando aplica.
- Ejecutaste `migrate` y probaste los flujos principales.

- No subiste `.env` ni datos sensibles.
