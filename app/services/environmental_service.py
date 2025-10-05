import requests
import math
import requests
from flask import current_app

class EnvironmentalService:
    """Servicio para calcular impactos ambientales usando datos USGS"""
    
    def __init__(self):
        self.usgs_earthquake_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'
    
    def calculate_environmental_impacts(self, impact_lat, impact_lon, energy_megatons, 
                                       crater_diameter_m, target_type='land'):
        """
        Calcula impactos ambientales detallados
        
        Returns:
            Dict con efectos atmosféricos, tsunamis, clima, ecosistema
        """
        impacts = {
            'atmospheric': self._calculate_atmospheric_effects(energy_megatons),
            'climate': self._calculate_climate_effects(energy_megatons),
            'tsunami': self._calculate_tsunami_effects(impact_lat, impact_lon, energy_megatons, target_type),
            'seismic': self._calculate_seismic_effects(energy_megatons),
            'ecosystem': self._calculate_ecosystem_damage(energy_megatons, crater_diameter_m),
            'radiation': self._calculate_radiation_effects(energy_megatons)
        }
        
        return impacts
    
    def _calculate_atmospheric_effects(self, energy_megatons):
        """Efectos atmosféricos del impacto"""
        
        if energy_megatons < 1:
            return {
                'severity': 'Minimal',
                'dust_ejected_tons': int(energy_megatons * 1e6),
                'atmospheric_penetration': 'Complete vaporization before impact',
                'shock_wave': 'Localized sonic boom',
                'effects': [
                    'Bright fireball visible',
                    'Loud sonic boom in area',
                    'Minimal dust in atmosphere'
                ]
            }
        elif energy_megatons < 100:
            return {
                'severity': 'Moderate',
                'dust_ejected_tons': int(energy_megatons * 5e6),
                'atmospheric_penetration': 'Significant energy release in atmosphere',
                'shock_wave': f'Overpressure up to {energy_megatons * 0.5:.1f} PSI at 10km',
                'effects': [
                    'Massive fireball visible for hundreds of km',
                    'Shockwave breaks windows up to 50km away',
                    'Dust cloud affects local weather for days',
                    'Temporary ozone depletion in region'
                ]
            }
        elif energy_megatons < 10000:
            return {
                'severity': 'Severe',
                'dust_ejected_tons': int(energy_megatons * 1e7),
                'atmospheric_penetration': 'Massive explosion in stratosphere',
                'shock_wave': f'Global atmospheric disturbance',
                'effects': [
                    'Fireball visible from space',
                    'Stratospheric dust injection',
                    'Regional cooling for weeks/months',
                    'Acid rain in surrounding areas',
                    'Ozone layer damage',
                    'Disruption of air travel globally'
                ]
            }
        else:
            return {
                'severity': 'Catastrophic',
                'dust_ejected_tons': int(energy_megatons * 5e7),
                'atmospheric_penetration': 'Mass extinction level event',
                'shock_wave': 'Global atmospheric ignition possible',
                'effects': [
                    'Global dust cloud blocking sunlight',
                    'Impact winter lasting years',
                    'Collapse of photosynthesis',
                    'Mass extinction of plant life',
                    'Breakdown of food chains',
                    'Global temperature drop of 10-20°C'
                ]
            }
    
    def _calculate_climate_effects(self, energy_megatons):
        """Efectos climáticos globales"""
        
        if energy_megatons < 100:
            duration_days = int(energy_megatons * 0.5)
            temp_drop_c = round(energy_megatons * 0.01, 2)
            
            return {
                'severity': 'Local',
                'duration_days': duration_days,
                'temperature_drop_celsius': temp_drop_c,
                'affected_area_km2': int(energy_megatons * 10000),
                'effects': [
                    f'Local cooling of {temp_drop_c}°C for {duration_days} days',
                    'Disruption of local weather patterns',
                    'Temporary reduction in solar radiation'
                ]
            }
        elif energy_megatons < 10000:
            duration_months = int(energy_megatons / 100)
            temp_drop_c = round(energy_megatons * 0.001, 1)
            
            return {
                'severity': 'Regional/Continental',
                'duration_months': duration_months,
                'temperature_drop_celsius': temp_drop_c,
                'affected_area_km2': int(energy_megatons * 100000),
                'effects': [
                    f'Regional cooling of {temp_drop_c}°C for {duration_months} months',
                    'Disruption of growing seasons',
                    'Increased precipitation in some areas, drought in others',
                    'Failure of crops over wide areas',
                    'Economic disruption to agriculture'
                ]
            }
        else:
            duration_years = int(energy_megatons / 10000)
            temp_drop_c = round(energy_megatons * 0.0001, 1)
            
            return {
                'severity': 'Global - Mass Extinction',
                'duration_years': duration_years,
                'temperature_drop_celsius': temp_drop_c,
                'affected_area_km2': 510000000,  # Toda la Tierra
                'effects': [
                    f'Global cooling of {temp_drop_c}°C for {duration_years}+ years',
                    'Impact winter - darkness for months',
                    'Collapse of global food production',
                    'Mass starvation',
                    'Ecosystem collapse',
                    'Possible human extinction'
                ]
            }
    
    def _calculate_tsunami_effects(self, lat, lon, energy_megatons, target_type):
        """Efectos de tsunami si impacta en océano"""
        
        if target_type != 'water':
            return {
                'risk': 'None',
                'message': 'Impact on land - no tsunami generated'
            }
        
        # Estimar altura de ola
        wave_height_m = 10 * (energy_megatons ** 0.5)
        
        if energy_megatons < 10:
            return {
                'risk': 'Low',
                'wave_height_meters': round(wave_height_m, 1),
                'affected_coastlines': 'Local (< 100km)',
                'effects': [
                    f'Tsunami waves up to {wave_height_m:.1f}m high',
                    'Flooding of immediate coastal areas',
                    'Damage to ports and coastal infrastructure',
                    'Evacuation needed for low-lying coasts'
                ]
            }
        elif energy_megatons < 1000:
            return {
                'risk': 'High',
                'wave_height_meters': round(wave_height_m, 1),
                'affected_coastlines': 'Regional (100-1000km)',
                'travel_time_hours': 'Varies by distance (6-12 hours typical)',
                'effects': [
                    f'Massive tsunami waves up to {wave_height_m:.1f}m high',
                    'Devastation of all coastal areas within 1000km',
                    'Waves detectable across ocean basin',
                    'Complete destruction of coastal cities',
                    'Millions at risk',
                    'Warning time: 2-12 hours depending on distance'
                ]
            }
        else:
            return {
                'risk': 'Catastrophic',
                'wave_height_meters': round(wave_height_m, 1),
                'affected_coastlines': 'Global - All oceans',
                'travel_time_hours': '12-24 hours to reach all coasts',
                'effects': [
                    f'Mega-tsunami waves up to {wave_height_m:.1f}m high',
                    'Global tsunami affecting all ocean-connected coasts',
                    'Complete inundation of coastal plains',
                    'Billions at risk',
                    'Permanent reshaping of coastlines',
                    'Flooding extends 10-100km inland'
                ]
            }
    
    def _calculate_seismic_effects(self, energy_megatons):
        """Efectos sísmicos globales"""
        
        magnitude = 0.67 * math.log10(energy_megatons * 4.184e15) - 5.87
        
        if magnitude < 5:
            return {
                'magnitude': round(magnitude, 1),
                'severity': 'Minor',
                'range_km': 50,
                'effects': ['Perceptible shaking near impact site']
            }
        elif magnitude < 7:
            return {
                'magnitude': round(magnitude, 1),
                'severity': 'Moderate',
                'range_km': 500,
                'effects': [
                    'Strong shaking up to 500km away',
                    'Damage to buildings near impact',
                    'Landslides in mountainous terrain',
                    'Infrastructure damage'
                ]
            }
        else:
            return {
                'magnitude': round(magnitude, 1),
                'severity': 'Extreme',
                'range_km': 5000,
                'effects': [
                    'Global seismic waves detectable',
                    'Severe shaking across continent',
                    'Triggering of earthquakes on fault lines',
                    'Massive landslides',
                    'Volcanic eruptions triggered',
                    'Permanent geological changes'
                ]
            }
    
    def _calculate_ecosystem_damage(self, energy_megatons, crater_diameter_m):
        """Daño al ecosistema"""
        
        if energy_megatons < 1:
            affected_area = int(crater_diameter_m * crater_diameter_m * 3.14 / 1e6)  # km²
            return {
                'severity': 'Localized',
                'affected_area_km2': affected_area,
                'habitat_loss': 'Minimal',
                'species_at_risk': 'Local populations only',
                'recovery_time': '5-20 years',
                'effects': [
                    'Destruction of immediate impact zone',
                    'Fire damage in surrounding forest',
                    'Temporary displacement of wildlife'
                ]
            }
        elif energy_megatons < 10000:
            affected_area = int(energy_megatons * 5000)
            return {
                'severity': 'Regional',
                'affected_area_km2': affected_area,
                'habitat_loss': 'Significant',
                'species_at_risk': 'Regional extinctions possible',
                'recovery_time': '50-200 years',
                'effects': [
                    'Widespread destruction of ecosystems',
                    'Mass animal deaths from shockwave and fires',
                    'Contamination of water sources',
                    'Disruption of food chains',
                    'Extinction of specialized species',
                    'Invasive species takeover during recovery'
                ]
            }
        else:
            return {
                'severity': 'Mass Extinction Event',
                'affected_area_km2': 510000000,  # Global
                'habitat_loss': 'Catastrophic - Global',
                'species_at_risk': '70-90% of all species',
                'recovery_time': 'Millions of years',
                'effects': [
                    'Collapse of global ecosystems',
                    'Extinction of most large animals',
                    'Death of most plant life (no sunlight)',
                    'Collapse of ocean food chains',
                    'Only extremophiles and some microbes survive',
                    'Complete restructuring of biosphere',
                    'Comparable to dinosaur extinction'
                ]
            }
    
    def _calculate_radiation_effects(self, energy_megatons):
        """Efectos de radiación térmica"""
        
        thermal_radius_km = 5.0 * (energy_megatons ** 0.4)
        
        if energy_megatons < 1:
            return {
                'thermal_radiation_radius_km': round(thermal_radius_km, 1),
                'severity': 'Low',
                'effects': [
                    'First-degree burns possible within 1km',
                    'Ignition of dry materials',
                    'Brief flash of intense light'
                ]
            }
        elif energy_megatons < 1000:
            return {
                'thermal_radiation_radius_km': round(thermal_radius_km, 1),
                'severity': 'High',
                'effects': [
                    f'Third-degree burns up to {thermal_radius_km:.0f}km from impact',
                    'Ignition of all flammable materials',
                    'Firestorms in urban areas',
                    'Retinal damage from flash (permanent blindness)',
                    'Widespread fires creating smoke and soot'
                ]
            }
        else:
            return {
                'thermal_radiation_radius_km': round(thermal_radius_km, 1),
                'severity': 'Extreme',
                'effects': [
                    f'Lethal thermal radiation up to {thermal_radius_km:.0f}km',
                    'Global heat pulse',
                    'Ignition of forests worldwide',
                    'Atmospheric heating',
                    'Possible global firestorm'
                ]
            }

import math