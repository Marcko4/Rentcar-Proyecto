# Rentcar - Proyecto de alquiler de vehículos

Proyecto Django para la materia. Incluye configuración inicial para PostgreSQL.

Pasos rápidos:

1. Crear y activar un entorno virtual:

   python -m venv .venv
   .venv\Scripts\activate

2. Instalar dependencias:

   pip install -r requirements.txt

3. Copiar `.env.example` a `.env` y ajustar variables (DATABASE_URL, SECRET_KEY)

4. Ejecutar migraciones y crear superusuario:

   python manage.py migrate
   python manage.py createsuperuser

5. Correr el servidor:

   python manage.py runserver
