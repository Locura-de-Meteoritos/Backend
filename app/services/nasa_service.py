import requests
from datetime import datetime, timedelta
from flask import current_app

class NASAService:
    """Servicio para interactuar con la NASA API"""
    
    def __init__(self):
        self.base_url = None
        self.api_key = None
    
    def _get_config(self):
        """Obtiene configuración de la app actual"""
        if not self.base_url:
            self.base_url = current_app.config['NASA_NEO_API_URL']
            self.api_key = current_app.config['NASA_API_KEY']
    
    def get_neo_feed(self, start_date=None, end_date=None):
        """
        Obtiene feed de asteroides cercanos a la Tierra
        
        Args:
            start_date: Fecha inicio (YYYY-MM-DD)
            end_date: Fecha fin (YYYY-MM-DD)
        
        Returns:
            Lista procesada de asteroides
        """
        self._get_config()
        
        # Fechas por defecto: hoy y próximos 7 días
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        if not end_date:
            end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        # Construir URL
        url = f"{self.base_url}/feed"
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'api_key': self.api_key
        }
        
        # Hacer petición
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Procesar y simplificar datos
        asteroids = []
        for date, objects in data.get('near_earth_objects', {}).items():
            for obj in objects:
                asteroids.append(self._format_asteroid(obj))
        
        return asteroids
    
    def _format_asteroid(self, raw_data):
        """
        Formatea datos crudos de NASA a estructura más simple
        """
        return {
            'id': raw_data.get('id'),
            'name': raw_data.get('name'),
            'diameter_min_m': raw_data['estimated_diameter']['meters']['estimated_diameter_min'],
            'diameter_max_m': raw_data['estimated_diameter']['meters']['estimated_diameter_max'],
            'is_potentially_hazardous': raw_data.get('is_potentially_hazardous_asteroid'),
            'close_approach_data': [
                {
                    'date': approach['close_approach_date'],
                    'velocity_km_s': float(approach['relative_velocity']['kilometers_per_second']),
                    'miss_distance_km': float(approach['miss_distance']['kilometers'])
                }
                for approach in raw_data.get('close_approach_data', [])
            ]
        }
    
    def get_asteroid_details(self, asteroid_id):
        """
        Obtiene detalles completos de un asteroide específico
        """
        self._get_config()
        
        url = f"{self.base_url}/neo/{asteroid_id}"
        params = {'api_key': self.api_key}
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        return self._format_asteroid(response.json())