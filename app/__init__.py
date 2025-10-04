from flask import Flask
from flask_cors import CORS
from config import config

def create_app(config_name='default'):
    """Factory function para crear la aplicación Flask"""
    
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Habilitar CORS (permite peticiones desde React)
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Registrar blueprints (rutas)
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Ruta de health check
    @app.route('/health')
    def health_check():
        return {'status': 'OK', 'message': 'AstroDefender API is running'}, 200
    
    return app