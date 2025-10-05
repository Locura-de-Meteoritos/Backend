import requests
from flask import current_app

class GeocodingService:
    """Servicio para geocodificación usando Distance Matrix AI"""
    
    def __init__(self):
        self.base_url = None
        self.api_key = None
    
    def _get_config(self):
        """Obtiene configuración de la app actual"""
        if not self.base_url:
            self.base_url = current_app.config['DISTANCEMATRIX_API_URL']
            self.api_key = current_app.config['DISTANCEMATRIX_API_KEY']
    
    def get_coordinates(self, address):
        """
        Obtiene coordenadas de una dirección o ciudad
        
        Args:
            address: Dirección completa, ciudad, o "Ciudad, País"
                    Ejemplos: 
                    - "São Paulo, Brazil"
                    - "New York, USA"
                    - "Tokyo, Japan"
        
        Returns:
            Dict con lat, lon y metadatos
        """
        self._get_config()
        
        try:
            url = f"{self.base_url}/geocode/json"
            params = {
                'address': address,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'OK' or not data.get('result'):
                return None
            
            # Tomar primer resultado
            result = data['result'][0]
            location = result['geometry']['location']
            
            # Extraer componentes de dirección
            address_components = {}
            for component in result.get('address_components', []):
                types = component.get('types', [])
                if 'locality' in types:
                    address_components['city'] = component['long_name']
                elif 'country' in types:
                    address_components['country'] = component['long_name']
                    address_components['country_code'] = component['short_name']
                elif 'administrative_area_level_1' in types:
                    address_components['state'] = component['long_name']
            
            return {
                'lat': location['lat'],
                'lon': location['lng'],
                'formatted_address': result.get('formatted_address'),
                'city': address_components.get('city'),
                'country': address_components.get('country'),
                'country_code': address_components.get('country_code'),
                'state': address_components.get('state'),
                'location_type': result['geometry'].get('location_type'),
                'place_id': result.get('place_id', '')
            }
            
        except Exception as e:
            print(f"Error geocoding {address}: {str(e)}")
            return None
    
    def reverse_geocode(self, lat, lon):
        """
        Obtiene dirección desde coordenadas (geocodificación inversa)
        
        Args:
            lat: Latitud
            lon: Longitud
        
        Returns:
            Dict con información de la ubicación
        """
        self._get_config()
        
        try:
            url = f"{self.base_url}/geocode/json"
            params = {
                'latlng': f"{lat},{lon}",
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'OK' or not data.get('result'):
                return None
            
            result = data['result'][0]
            
            # Extraer componentes
            address_components = {}
            for component in result.get('address_components', []):
                types = component.get('types', [])
                if 'locality' in types:
                    address_components['city'] = component['long_name']
                elif 'country' in types:
                    address_components['country'] = component['long_name']
                elif 'administrative_area_level_1' in types:
                    address_components['state'] = component['long_name']
            
            return {
                'formatted_address': result.get('formatted_address'),
                'city': address_components.get('city'),
                'country': address_components.get('country'),
                'state': address_components.get('state')
            }
            
        except Exception as e:
            print(f"Error reverse geocoding ({lat}, {lon}): {str(e)}")
            return None
    
    def find_cities_in_radius(self, lat, lon, radius_km):
        """
        Encuentra ciudades cercanas usando Places API
        
        Nota: Distance Matrix AI no tiene Places API integrada.
        Para producción, necesitarías una base de datos de ciudades
        o usar otra API complementaria.
        
        Esta es una implementación simplificada con ciudades hardcodeadas
        para el hackathon.
        """
        # Base de datos simplificada de ciudades importantes
        major_cities = [
            {'name': 'São Paulo', 'lat': -23.5505, 'lon': -46.6333, 'country': 'Brazil', 'population': 12300000},
            {'name': 'Rio de Janeiro', 'lat': -22.9068, 'lon': -43.1729, 'country': 'Brazil', 'population': 6748000},
            {'name': 'New York', 'lat': 40.7128, 'lon': -74.0060, 'country': 'USA', 'population': 8336000},
            {'name': 'Los Angeles', 'lat': 34.0522, 'lon': -118.2437, 'country': 'USA', 'population': 3979000},
            {'name': 'Tokyo', 'lat': 35.6762, 'lon': 139.6503, 'country': 'Japan', 'population': 13960000},
            {'name': 'London', 'lat': 51.5074, 'lon': -0.1278, 'country': 'UK', 'population': 8982000},
            {'name': 'Paris', 'lat': 48.8566, 'lon': 2.3522, 'country': 'France', 'population': 2161000},
            {'name': 'Mexico City', 'lat': 19.4326, 'lon': -99.1332, 'country': 'Mexico', 'population': 9209000},
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'country': 'India', 'population': 20411000},
            {'name': 'Beijing', 'lat': 39.9042, 'lon': 116.4074, 'country': 'China', 'population': 21540000},
            {'name': 'Moscow', 'lat': 55.7558, 'lon': 37.6173, 'country': 'Russia', 'population': 12506000},
            {'name': 'Cairo', 'lat': 30.0444, 'lon': 31.2357, 'country': 'Egypt', 'population': 9500000},
            {'name': 'Sydney', 'lat': -33.8688, 'lon': 151.2093, 'country': 'Australia', 'population': 5312000},
            {'name': 'Buenos Aires', 'lat': -34.6037, 'lon': -58.3816, 'country': 'Argentina', 'population': 15180000},
            {'name': 'Lima', 'lat': -12.0464, 'lon': -77.0428, 'country': 'Peru', 'population': 10719000},
        ]
        
        import math
        
        def haversine_distance(lat1, lon1, lat2, lon2):
            R = 6371  # Radio de la Tierra en km
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = (math.sin(delta_lat / 2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lon / 2) ** 2)
            
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return R * c
        
        # Filtrar ciudades dentro del radio
        nearby = []
        for city in major_cities:
            distance = haversine_distance(lat, lon, city['lat'], city['lon'])
            if distance <= radius_km:
                nearby.append({
                    'name': city['name'],
                    'lat': city['lat'],
                    'lon': city['lon'],
                    'country': city['country'],
                    'population': city['population'],
                    'distance_km': round(distance, 2)
                })
        
        # Ordenar por distancia
        nearby.sort(key=lambda x: x['distance_km'])
        
        return nearby