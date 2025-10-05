from flask import Blueprint

# Crear blueprint para las rutas API
api_bp = Blueprint('api', __name__)

# Importar rutas específicas (AL FINAL)
from app.routes import asteroids
from app.routes import impact