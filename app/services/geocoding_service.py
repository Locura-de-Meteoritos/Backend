import math
import requests
from flask import current_app
import math

class GeocodingService:
    """Servicio para geocodificación usando Distance Matrix AI + Overpass"""
    
    def __init__(self):
        self.base_url = None
        self.api_key = None
        self.overpass_url = "https://overpass-api.de/api/interpreter"
    
    def _get_config(self):
        """Obtiene configuración de la app actual"""
        if not self.base_url:
            self.base_url = current_app.config['DISTANCEMATRIX_API_URL']
            self.api_key = current_app.config['DISTANCEMATRIX_API_KEY']
    
    def get_coordinates(self, address):
        """Obtiene coordenadas usando Distance Matrix AI"""
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
            
            result = data['result'][0]
            location = result['geometry']['location']
            
            address_components = {}
            for component in result.get('address_components', []) or []:
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
                'state': address_components.get('state')
            }
            
        except Exception as e:
            print(f"Error geocoding {address}: {str(e)}")
            return None
    
    def reverse_geocode(self, lat, lon):
        """
        Geocodificación inversa con detección de océanos
        """
        self._get_config()
        
        try:
            # Intentar con Distance Matrix AI
            url = f"{self.base_url}/geocode/json"
            params = {
                'latlng': f"{lat},{lon}",
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'OK' and data.get('result'):
                result = data['result'][0]
                
                if result.get('address_components'):
                    address_components = {}
                    for component in result['address_components']:
                        types = component.get('types', [])
                        if 'locality' in types:
                            address_components['city'] = component['long_name']
                        elif 'country' in types:
                            address_components['country'] = component['long_name']
                            address_components['country_code'] = component['short_name']
                        elif 'administrative_area_level_1' in types:
                            address_components['state'] = component['long_name']
                    
                    if address_components.get('city'):
                        return {
                            'formatted_address': result.get('formatted_address', 'Unknown'),
                            'city': address_components.get('city'),
                            'country': address_components.get('country'),
                            'country_code': address_components.get('country_code'),
                            'state': address_components.get('state'),
                            'is_remote': False,
                            'is_ocean': False
                        }
            
            # Fallback a Overpass (detecta océanos también)
            return self._find_nearest_city_overpass(lat, lon)
            
        except Exception as e:
            print(f"Error en reverse_geocode: {e}")
            return self._find_nearest_city_overpass(lat, lon)
    
    def _find_nearest_city_overpass(self, lat, lon):
        """
        Encuentra la ciudad más cercana o detecta si es océano
        """
        try:
            # Buscar en radios progresivos
            for radius_km in [50, 100, 200, 500]:
                query = f"""
                [out:json][timeout:15];
                (
                  node["place"="city"](around:{radius_km * 1000},{lat},{lon});
                  node["place"="town"](around:{radius_km * 1000},{lat},{lon});
                );
                out body 1;
                """
                
                response = requests.post(
                    self.overpass_url,
                    data={'data': query},
                    timeout=20
                )
                
                if response.status_code == 200:
                    data = response.json()
                    elements = data.get('elements', [])
                    
                    if elements:
                        nearest = elements[0]
                        city_name = nearest['tags'].get('name', 'Unknown')
                        city_lat = nearest.get('lat')
                        city_lon = nearest.get('lon')
                        
                        distance = self._haversine_distance(lat, lon, city_lat, city_lon)
                        
                        # Si la ciudad más cercana está a más de 300km, probablemente es océano
                        if distance > 300:
                            return self._identify_ocean_or_sea(lat, lon, city_name, distance)
                        
                        return {
                            'formatted_address': f"Near {city_name} (~{int(distance)}km away)",
                            'city': city_name,
                            'country': nearest['tags'].get('addr:country', 'Unknown'),
                            'country_code': None,
                            'state': nearest['tags'].get('addr:state'),
                            'is_remote': True,
                            'is_ocean': False,
                            'nearest_city_distance_km': round(distance, 2)
                        }
            
            # No encontró ciudades en 500km = probablemente océano
            return self._identify_ocean_or_sea(lat, lon, None, None)
            
        except Exception as e:
            print(f"Error en Overpass fallback: {e}")
            return None

    def _identify_ocean_or_sea(self, lat, lon, nearest_city=None, distance=None):
        """
        Identifica qué océano/mar es según coordenadas
        """
        # Determinar océano por ubicación geográfica aproximada
        ocean_name = "Unknown Ocean"
        
        # Océano Pacífico
        if -180 <= lon <= -70 or 120 <= lon <= 180:
            if -60 <= lat <= 60:
                ocean_name = "Pacific Ocean"
        
        # Océano Atlántico
        elif -70 <= lon <= 20:
            if -60 <= lat <= 70:
                ocean_name = "Atlantic Ocean"
        
        # Océano Índico
        elif 20 <= lon <= 120:
            if -60 <= lat <= 30:
                ocean_name = "Indian Ocean"
        
        # Océano Ártico
        if lat > 66:
            ocean_name = "Arctic Ocean"
        
        # Océano Antártico
        elif lat < -60:
            ocean_name = "Southern Ocean"
        
        # Casos especiales: Mares
        if 30 <= lat <= 45 and -10 <= lon <= 45:
            ocean_name = "Mediterranean Sea"
        elif 10 <= lat <= 30 and 35 <= lon <= 75:
            ocean_name = "Arabian Sea"
        elif 0 <= lat <= 25 and 90 <= lon <= 100:
            ocean_name = "Bay of Bengal"
        elif 20 <= lat <= 50 and 120 <= lon <= 145:
            ocean_name = "Sea of Japan"
        
        result = {
            'formatted_address': ocean_name,
            'city': None,
            'country': None,
            'country_code': None,
            'state': None,
            'is_remote': True,
            'is_ocean': True,
            'ocean_name': ocean_name
        }
        
        if nearest_city and distance:
            result['nearest_city'] = nearest_city
            result['nearest_city_distance_km'] = round(distance, 2)
            result['formatted_address'] = f"{ocean_name} (nearest city: {nearest_city}, ~{int(distance)}km away)"
        
        return result

    def find_cities_in_radius(self, lat, lon, radius_km):
        """
        Encuentra TODAS las ciudades cercanas usando Overpass API
            """
        try:
                query = f"""
                [out:json][timeout:25];
                (
                node["place"="city"](around:{radius_km * 1000},{lat},{lon});
                node["place"="town"](around:{radius_km * 1000},{lat},{lon});
                node["place"="village"](around:{radius_km * 1000},{lat},{lon});
                );
                out body;
                """
                
                response = requests.post(
                    self.overpass_url,
                    data={'data': query},
                    timeout=30
                )
                response.raise_for_status()
                
                data = response.json()
                cities = []
                
                for element in data.get('elements', []):
                    city_lat = element.get('lat')
                    city_lon = element.get('lon')
                    
                    if not city_lat or not city_lon:
                        continue
                    
                    distance = self._haversine_distance(lat, lon, city_lat, city_lon)
                    
                    cities.append({
                        'name': element['tags'].get('name', 'Unknown'),
                        'lat': city_lat,
                        'lon': city_lon,
                        'place_type': element['tags'].get('place'),
                        'population': element['tags'].get('population', 'Unknown'),
                        'country': element['tags'].get('addr:country', 
                                element['tags'].get('is_in:country', 'Unknown')),
                        'distance_km': round(distance, 2)
                    })
                
                cities.sort(key=lambda x: x['distance_km'])
                return cities[:50]
                
        except Exception as e:
                print(f"Error finding cities: {e}")
                return []
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
            """Calcula distancia entre dos puntos"""
            R = 6371
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            a = (math.sin(delta_lat / 2) ** 2 + 
                math.cos(lat1_rad) * math.cos(lat2_rad) * 
                math.sin(delta_lon / 2) ** 2)
            
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            return R * c