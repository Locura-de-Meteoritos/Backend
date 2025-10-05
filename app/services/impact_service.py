from app.utils.physics import ImpactPhysics

class ImpactService:
    """
    Servicio para calcular las consecuencias de un impacto de asteroide
    
    Este servicio toma datos de un asteroide (de la NASA API)
    y calcula todos los efectos del impacto
    """
    
    def __init__(self):
        self.physics = ImpactPhysics()
    
    def simulate_impact(self, diameter_m, velocity_km_s, impact_lat, impact_lon, 
                       impact_angle=45, target_type='land'):
        """
        Simula un impacto de asteroide completo
        
        Args:
            diameter_m: Diámetro del asteroide en metros (de NASA API)
            velocity_km_s: Velocidad en km/s (de NASA API)
            impact_lat: Latitud del punto de impacto
            impact_lon: Longitud del punto de impacto
            impact_angle: Ángulo de impacto (45° es promedio)
            target_type: 'land' o 'water'
        
        Returns:
            Dict con todos los resultados de la simulación
        """
        
        # PASO 1: Calcular masa del asteroide
        mass_kg = self.physics.calculate_mass(diameter_m)
        
        # PASO 2: Calcular energía del impacto
        energy_joules = self.physics.calculate_kinetic_energy(mass_kg, velocity_km_s)
        energy_megatons = self.physics.energy_to_tnt_megatons(energy_joules)
        
        # PASO 3: Calcular tamaño del cráter
        crater_diameter_m = self.physics.calculate_crater_diameter(
            energy_megatons, 
            target_type
        )
        
        # PASO 4: Calcular magnitud sísmica
        seismic_magnitude = self.physics.calculate_seismic_magnitude(energy_joules)
        
        # PASO 5: Calcular zonas de daño
        damage_radii = self.physics.calculate_damage_radii(energy_megatons)
        
        # PASO 6: Estructurar resultados
        results = {
            'asteroid': {
                'diameter_m': diameter_m,
                'mass_kg': mass_kg,
                'velocity_km_s': velocity_km_s
            },
            'impact': {
                'location': {
                    'lat': impact_lat,
                    'lon': impact_lon
                },
                'angle_degrees': impact_angle,
                'target_type': target_type
            },
            'energy': {
                'joules': energy_joules,
                'megatons_tnt': round(energy_megatons, 2),
                'hiroshima_bombs': round(energy_megatons / 0.015, 0),
                'comparison': self._get_energy_comparison(energy_megatons)
            },
            'crater': {
                'diameter_m': round(crater_diameter_m, 2),
                'radius_m': round(crater_diameter_m / 2, 2),
                'comparison': self._get_crater_comparison(crater_diameter_m)
            },
            'seismic': {
                'magnitude_richter': round(seismic_magnitude, 2),
                'comparison': self._get_seismic_comparison(seismic_magnitude)
            },
            'damage_zones': {
                'crater_radius_km': round(damage_radii['crater_radius_km'], 2),
                'fireball_radius_km': round(damage_radii['fireball_radius_km'], 2),
                'shockwave_radius_km': round(damage_radii['shockwave_radius_km'], 2),
                'thermal_radiation_km': round(damage_radii['thermal_radiation_km'], 2),
                'seismic_effect_km': round(damage_radii['seismic_effect_km'], 2)
            },
            'population_impact': self._estimate_population_impact(damage_radii)
        }
        
        return results
    
    def simulate_from_nasa_data(self, asteroid_data, impact_lat, impact_lon, target_type='land'):
        """
        Simula impacto usando datos directamente de la NASA API
        
        Args:
            asteroid_data: Objeto con datos de NASA (como el que recibiste)
            impact_lat: Latitud del impacto
            impact_lon: Longitud del impacto
            target_type: 'land' o 'water'
        
        Returns:
            Resultados de simulación
        
        Ejemplo de uso:
            asteroid = {
                "diameter_max_m": 701.52,
                "diameter_min_m": 313.73,
                "close_approach_data": [{
                    "velocity_km_s": 18.29
                }]
            }
            results = service.simulate_from_nasa_data(asteroid, -23.55, -46.63)
        """
        # Usar diámetro promedio
        diameter_max = asteroid_data.get('diameter_max_m', 0)
        diameter_min = asteroid_data.get('diameter_min_m', 0)
        diameter_avg = (diameter_max + diameter_min) / 2
        
        # Obtener velocidad del primer close approach
        close_approach = asteroid_data.get('close_approach_data', [{}])[0]
        velocity = close_approach.get('velocity_km_s', 20)  # Default 20 km/s
        
        # Simular con estos datos
        return self.simulate_impact(
            diameter_m=diameter_avg,
            velocity_km_s=velocity,
            impact_lat=impact_lat,
            impact_lon=impact_lon,
            target_type=target_type
        )
    
    def _get_energy_comparison(self, megatons):
        """Comparaciones de energía con eventos conocidos"""
        if megatons < 0.001:
            return "Menos que una bomba pequeña"
        elif megatons < 0.015:
            return "Similar a bombas convencionales grandes"
        elif megatons < 1:
            return f"Equivale a {megatons/0.015:.0f} bombas de Hiroshima"
        elif megatons < 50:
            return f"Mayor que cualquier bomba nuclear probada (Tsar Bomba: 50 MT)"
        else:
            return f"Equivale a {megatons:.0f} megatones - Evento de extinción"
    
    def _get_crater_comparison(self, diameter_m):
        """Comparaciones de tamaño de cráter"""
        if diameter_m < 50:
            return "Tamaño de una casa pequeña"
        elif diameter_m < 100:
            return "Tamaño de una cancha de fútbol"
        elif diameter_m < 500:
            return "Tamaño de varios campos de fútbol"
        elif diameter_m < 1000:
            return "Más grande que 10 manzanas de ciudad"
        elif diameter_m < 5000:
            return "Más grande que el Central Park de Nueva York"
        else:
            return f"Aproximadamente {diameter_m/1000:.1f} km de diámetro - Visible desde el espacio"
    
    def _get_seismic_comparison(self, magnitude):
        """Comparaciones de magnitud sísmica"""
        if magnitude < 3:
            return "Apenas detectable - solo instrumentos"
        elif magnitude < 4:
            return "Perceptible cerca del epicentro"
        elif magnitude < 5:
            return "Daño menor a edificios débiles"
        elif magnitude < 6:
            return "Daño moderado a estructuras"
        elif magnitude < 7:
            return "Daño severo en área amplia"
        elif magnitude < 8:
            return "Devastación mayor (similar a Haití 2010, 7.0)"
        else:
            return "Catastrófico (similar a Japón 2011, 9.1)"
    
    def _estimate_population_impact(self, damage_radii):
        """
        Estimación simplificada de población afectada
        
        Nota: En versión completa, usarías WorldPop API o datos de densidad real
        """
        # Usar densidad poblacional promedio global: ~60 personas/km²
        shockwave_area = 3.14159 * (damage_radii['shockwave_radius_km'] ** 2)
        estimated_affected = int(shockwave_area * 60)
        
        return {
            'method': 'simplified_average',
            'estimated_people_affected': estimated_affected,
            'affected_area_km2': round(shockwave_area, 2),
            'note': 'Estimación usando densidad promedio global. Integrar API de población para precisión.'
        }