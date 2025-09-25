# Tarea3_PDC

Inicializacion y dependencias
uv init
uv add fastapi --extra standard
uv add sqlalchemy
uv add python-dotenv

Dentro del .env.example se encuentra como escribir la clave para el verdadero .env que tiene una estructura asi
API_KEY=<VALOR_AQUI>

La app se puede correr usando
uv run fastaapi dev main.py

Endpoints
POST /api/v1/users/ → Crear usuario

PUT /api/v1/users/{user_id} → Actualizar usuario

GET /api/v1/users/{user_id} → Obtener usuario

DELETE /api/v1/users/{user_id} → Eliminar usuario


Ejemplos de request (postman)
GET 127.0.0.1:8000/api/v1/users/1

DELETE 127.0.0.1:8000/api/v1/users/5
