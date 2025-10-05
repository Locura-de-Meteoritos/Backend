from flask import jsonify, request
from app.routes import api_bp
from app.services.impact_service import ImpactService

# Crear instancia del servicio
impact_service = ImpactService()

@api_bp.route('/impact/simulate', methods=['POST'])
def simulate_impact():
    """
    Simula el impacto de un asteroide
    
    Endpoint: POST /api/impact/simulate
    
    Body JSON:
    {
        "diameter_m": 250,
        "velocity_km_s": 20,
        "impact_location": {
            "lat": -23.5505,
            "lon": -46.6333
        },
        "target_type": "land"
    }
    
    O también puedes enviar datos directos de NASA:
    {
        "nasa_data": {
            "diameter_max_m": 701.52,
            "diameter_min_m": 313.73,
            "close_approach_data": [{
                "velocity_km_s": 18.29
            }]
        },
        "impact_location": {
            "lat": -23.5505,
            "lon": -46.6333
        },
        "target_type": "land"
    }
    """
    try:
        data = request.get_json()
        
        # Validar que tenemos location
        if 'impact_location' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing impact_location'
            }), 400
        
        impact_lat = data['impact_location']['lat']
        impact_lon = data['impact_location']['lon']
        target_type = data.get('target_type', 'land')
        
        # OPCIÓN 1: Si enviaron datos de NASA directamente
        if 'nasa_data' in data:
            results = impact_service.simulate_from_nasa_data(
                asteroid_data=data['nasa_data'],
                impact_lat=impact_lat,
                impact_lon=impact_lon,
                target_type=target_type
            )
        
        # OPCIÓN 2: Si enviaron parámetros específicos
        elif 'diameter_m' in data and 'velocity_km_s' in data:
            results = impact_service.simulate_impact(
                diameter_m=data['diameter_m'],
                velocity_km_s=data['velocity_km_s'],
                impact_lat=impact_lat,
                impact_lon=impact_lon,
                impact_angle=data.get('impact_angle', 45),
                target_type=target_type
            )
        
        else:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: diameter_m and velocity_km_s, or nasa_data'
            }), 400
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/impact/simulate-asteroid/<asteroid_id>', methods=['POST'])
def simulate_asteroid_impact(asteroid_id):
    """
    Simula impacto de un asteroide específico de la NASA API
    
    Endpoint: POST /api/impact/simulate-asteroid/2247517
    
    Body JSON:
    {
        "impact_location": {
            "lat": -23.5505,
            "lon": -46.6333
        },
        "target_type": "land"
    }
    
    Este endpoint:
    1. Busca el asteroide en tu lista de NASA
    2. Extrae sus datos
    3. Simula el impacto
    """
    try:
        from app.services.nasa_service import NASAService
        
        data = request.get_json()
        
        # Validar location
        if 'impact_location' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing impact_location'
            }), 400
        
        # Obtener datos del asteroide
        nasa_service = NASAService()
        asteroid_data = nasa_service.get_asteroid_details(asteroid_id)
        
        # Simular impacto
        results = impact_service.simulate_from_nasa_data(
            asteroid_data=asteroid_data,
            impact_lat=data['impact_location']['lat'],
            impact_lon=data['impact_location']['lon'],
            target_type=data.get('target_type', 'land')
        )
        
        # Agregar info del asteroide
        results['asteroid_info'] = {
            'id': asteroid_data['id'],
            'name': asteroid_data['name'],
            'is_potentially_hazardous': asteroid_data['is_potentially_hazardous']
        }
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500