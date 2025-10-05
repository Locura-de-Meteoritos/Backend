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
    

@api_bp.route('/geocode', methods=['GET'])
def geocode_address():
    """
    Geocodifica una dirección o ciudad
    
    GET /api/geocode?address=São Paulo, Brazil
    GET /api/geocode?address=New York, USA
    """
    try:
        from app.services.geocoding_service import GeocodingService
        
        address = request.args.get('address')
        
        if not address:
            return jsonify({
                'success': False,
                'error': 'Missing address parameter'
            }), 400
        
        geocoding = GeocodingService()
        result = geocoding.get_coordinates(address)
        
        if not result:
            return jsonify({
                'success': False,
                'error': f'Address "{address}" not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/reverse-geocode', methods=['GET'])
def reverse_geocode():
    """
    Geocodificación inversa: obtiene dirección desde coordenadas
    
    GET /api/reverse-geocode?lat=-23.5505&lon=-46.6333
    """
    try:
        from app.services.geocoding_service import GeocodingService
        
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        
        if lat is None or lon is None:
            return jsonify({
                'success': False,
                'error': 'Missing lat or lon parameters'
            }), 400
        
        geocoding = GeocodingService()
        result = geocoding.reverse_geocode(lat, lon)
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Location not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/impact/simulate-city', methods=['POST'])
def simulate_city_impact():
    """
    Simula el impacto de un asteroide en una ciudad específica
    
    Endpoint: POST /api/impact/simulate-city
    
    Body JSON:
    {
        "city_name": "São Paulo, Brazil",
        "diameter_m": 500,
        "velocity_km_s": 20,
        "target_type": "land"
    }
    
    Este endpoint:
    1. Geocodifica la ciudad
    2. Simula el impacto
    3. Encuentra ciudades afectadas
    """
    try:
        from app.services.geocoding_service import GeocodingService
        
        data = request.get_json()
        
        # Validar datos requeridos
        if 'city_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing city_name'
            }), 400
            
        if 'diameter_m' not in data or 'velocity_km_s' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing diameter_m and velocity_km_s'
            }), 400
        
        # Geocodificar la ciudad
        geocoding = GeocodingService()
        location = geocoding.get_coordinates(data['city_name'])
        
        if not location:
            return jsonify({
                'success': False,
                'error': f'Could not find coordinates for {data["city_name"]}'
            }), 400
        
        impact_lat = location['lat']
        impact_lon = location['lon']
        
        # Simular el impacto
        results = impact_service.simulate_impact(
            diameter_m=data['diameter_m'],
            velocity_km_s=data['velocity_km_s'],
            impact_lat=impact_lat,
            impact_lon=impact_lon,
            target_type=data.get('target_type', 'land')
        )
        
        # Encontrar ciudades afectadas
        max_radius = max(
            results['damage_zones']['shockwave_radius_km'],
            results['damage_zones']['thermal_radiation_km'],
            results['damage_zones']['seismic_effect_km']
        )
        
        affected_cities = geocoding.find_cities_in_radius(
            impact_lat, 
            impact_lon, 
            max_radius
        )
        
        # Clasificar daño por ciudad
        for city in affected_cities:
            distance = city['distance_km']
            
            if distance <= results['damage_zones']['crater_radius_km']:
                city['damage_level'] = 'total_destruction'
                city['effects'] = 'Destrucción total - Vaporización inmediata'
            elif distance <= results['damage_zones']['fireball_radius_km']:
                city['damage_level'] = 'extreme'
                city['effects'] = 'Destrucción extrema - Incineración total'
            elif distance <= results['damage_zones']['shockwave_radius_km']:
                city['damage_level'] = 'severe'
                city['effects'] = 'Daño severo - Colapso de edificios, bajas masivas'
            elif distance <= results['damage_zones']['thermal_radiation_km']:
                city['damage_level'] = 'moderate'
                city['effects'] = 'Daño moderado - Quemaduras, incendios, estructuras dañadas'
            elif distance <= results['damage_zones']['seismic_effect_km']:
                city['damage_level'] = 'minor'
                city['effects'] = 'Daño menor - Ventanas rotas, temblores perceptibles'
            else:
                city['damage_level'] = 'minimal'
                city['effects'] = 'Efectos mínimos - Vibraciones menores'
        
        # Respuesta en el formato esperado
        response_data = {
            'impact': {
                'location': {
                    'lat': impact_lat,
                    'lon': impact_lon,
                    'city': location.get('city'),
                    'country': location.get('country'),
                    'formatted_address': location.get('formatted_address')
                },
                'asteroid': {
                    'diameter_m': data['diameter_m'],
                    'velocity_km_s': data['velocity_km_s'],
                    'target_type': data.get('target_type', 'land')
                },
                'energy': results['energy'],
                'crater': results['crater'],
                'damage_zones': results['damage_zones']
            },
            'affected_cities': [{
                'city': city['name'],
                'country': city['country'],
                'population': city['population'],
                'distance_from_impact_km': city['distance_km'],
                'damage_level': city['damage_level'],
                'effects': city['effects']
            } for city in affected_cities],
            'total_cities_affected': len(affected_cities)
        }
        
        return jsonify({
            'success': True,
            'data': response_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500