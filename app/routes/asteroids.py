from flask import jsonify, request
from app.routes import api_bp
from app.services.nasa_service import NASAService

# Instancia del servicio
nasa_service = NASAService()

@api_bp.route('/asteroids/near-earth', methods=['GET'])
def get_near_earth_asteroids():
    """
    Obtiene lista de asteroides cercanos a la Tierra
    
    Query params:
    - start_date: fecha inicio (YYYY-MM-DD)
    - end_date: fecha fin (YYYY-MM-DD)
    """
    try:
        # Obtener parámetros de la petición
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Llamar al servicio de NASA
        asteroids = nasa_service.get_neo_feed(start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': asteroids
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/asteroids/<asteroid_id>', methods=['GET'])
def get_asteroid_details(asteroid_id):
    """
    Obtiene detalles de un asteroide específico
    """
    try:
        details = nasa_service.get_asteroid_details(asteroid_id)
        
        return jsonify({
            'success': True,
            'data': details
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404