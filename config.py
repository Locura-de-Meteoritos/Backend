import os
from dotenv import load_dotenv

# Carga variables de entorno
load_dotenv()

class Config:
    """Configuración base de la aplicación"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    NASA_API_KEY = os.environ.get('NASA_API_KEY') or 'DEMO_KEY'
    DISTANCEMATRIX_API_KEY = os.environ.get('DISTANCEMATRIX_API_KEY') or 'DEMO_KEY'
    
    # URLs de APIs externas
    NASA_NEO_API_URL = 'https://api.nasa.gov/neo/rest/v1'
    USGS_EARTHQUAKE_API_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    DISTANCEMATRIX_API_URL = 'https://api.distancematrix.ai/maps/api'  # NUEVO
    
    # CORS (permite peticiones desde React)
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173']
    
    # Límites de rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per hour"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}