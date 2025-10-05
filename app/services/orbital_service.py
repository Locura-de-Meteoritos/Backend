import math
from datetime import datetime, timedelta

class OrbitalService:
    """Servicio para cálculos orbitales y tiempo de impacto"""
    
    # Constantes astronómicas
    AU_TO_KM = 149597870.7  # 1 AU en kilómetros
    EARTH_RADIUS = 6371  # km
    
    def calculate_time_to_impact(self, asteroid_data):
        """
        Calcula tiempo hasta el impacto basado en datos de close approach
        
        Args:
            asteroid_data: Datos del asteroide de NASA API con close_approach_data
        
        Returns:
            Dict con tiempo hasta impacto y recomendaciones de evacuación
        """
        close_approaches = asteroid_data.get('close_approach_data', [])
        
        if not close_approaches:
            return {
                'has_approach_data': False,
                'message': 'No close approach data available'
            }
        
        # Tomar el approach más cercano
        next_approach = close_approaches[0]
        
        approach_date_str = next_approach.get('close_approach_date_full') or next_approach.get('close_approach_date')
        miss_distance_km = float(next_approach.get('miss_distance', {}).get('kilometers', 0))
        velocity_km_s = float(next_approach.get('relative_velocity', {}).get('kilometers_per_second', 0))
        
        # Verificar que tenemos fecha válida
        if not approach_date_str:
            return {
                'has_approach_data': False,
                'message': 'No valid approach date found'
            }
        
        # Parsear fecha
        try:
            if 'T' in approach_date_str:
                approach_date = datetime.strptime(approach_date_str, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                approach_date = datetime.strptime(approach_date_str, '%Y-%m-%d')
        except:
            try:
                approach_date = datetime.strptime(approach_date_str.split('T')[0], '%Y-%m-%d')
            except:
                return {
                    'has_approach_data': False,
                    'message': f'Invalid date format: {approach_date_str}'
                }
        
        # Calcular tiempo restante
        now = datetime.utcnow()
        time_delta = approach_date - now
        
        days_until = time_delta.days
        hours_until = time_delta.seconds // 3600
        minutes_until = (time_delta.seconds % 3600) // 60
        
        # Calcular si impactará (miss_distance < radio Tierra)
        will_impact = miss_distance_km < self.EARTH_RADIUS
        
        # Recomendaciones de evacuación
        evacuation_status = self._get_evacuation_recommendations(days_until, will_impact)
        
        return {
            'has_approach_data': True,
            'approach_date': approach_date.isoformat(),
            'approach_date_formatted': approach_date.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'time_until_approach': {
                'total_seconds': time_delta.total_seconds(),
                'days': days_until,
                'hours': hours_until,
                'minutes': minutes_until,
                'formatted': f"{days_until}d {hours_until}h {minutes_until}m"
            },
            'miss_distance_km': miss_distance_km,
            'velocity_km_s': velocity_km_s,
            'will_impact': will_impact,
            'impact_probability': 'High' if will_impact else 'Very Low',
            'evacuation': evacuation_status
        }
    
    def _get_evacuation_recommendations(self, days_until, will_impact):
        """
        Genera recomendaciones de evacuación según tiempo disponible
        """
        if not will_impact:
            return {
                'required': False,
                'status': 'No evacuation needed',
                'level': 'Green',
                'message': 'Asteroid will safely pass by Earth'
            }
        
        if days_until < 0:
            return {
                'required': True,
                'status': 'IMPACT OCCURRED',
                'level': 'Black',
                'message': 'Impact has already occurred'
            }
        elif days_until < 1:
            return {
                'required': True,
                'status': 'IMMEDIATE EVACUATION',
                'level': 'Red',
                'message': 'Less than 24 hours until impact. Seek immediate shelter in designated safe zones.',
                'actions': [
                    'Move to underground shelters immediately',
                    'Stay away from windows and coastal areas',
                    'Follow emergency services instructions',
                    'Ensure emergency supplies (water, food, medical kit)'
                ]
            }
        elif days_until < 7:
            return {
                'required': True,
                'status': 'CRITICAL - Begin evacuation',
                'level': 'Red',
                'message': f'{days_until} days until impact. Evacuate impact zone immediately.',
                'actions': [
                    'Leave impact zone and surrounding areas (500+ km radius)',
                    'Travel inland if near coast (tsunami risk)',
                    'Stock emergency supplies for 2+ weeks',
                    'Follow official evacuation routes',
                    'Keep communication devices charged'
                ]
            }
        elif days_until < 30:
            return {
                'required': True,
                'status': 'High Alert - Prepare to evacuate',
                'level': 'Orange',
                'message': f'{days_until} days until impact. Prepare evacuation plan.',
                'actions': [
                    'Identify evacuation routes and safe zones',
                    'Prepare emergency kit (documents, supplies, medications)',
                    'Plan transportation and accommodation',
                    'Monitor official channels for updates',
                    'Coordinate with family and community'
                ]
            }
        elif days_until < 180:
            return {
                'required': False,
                'status': 'Elevated - Monitor situation',
                'level': 'Yellow',
                'message': f'{days_until} days until potential impact. Stay informed.',
                'actions': [
                    'Monitor news and official warnings',
                    'Review family emergency plan',
                    'Identify potential evacuation destinations',
                    'Maintain emergency supplies',
                    'Await deflection mission results'
                ]
            }
        else:
            return {
                'required': False,
                'status': 'Advisory - Mitigation possible',
                'level': 'Green',
                'message': f'{days_until} days until approach. Time for deflection missions.',
                'actions': [
                    'Space agencies can attempt deflection',
                    'Monitor trajectory updates',
                    'Public awareness campaigns',
                    'Scientific community coordination'
                ]
            }