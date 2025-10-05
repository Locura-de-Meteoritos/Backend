import math

import math

class ImpactPhysics:
    """Cálculos físicos para simulación de impactos de asteroides"""
    
    # Constantes físicas
    ASTEROID_DENSITY = 3000  # kg/m³ (roca típica)
    TNT_JOULES = 4.184e9  # Joules por tonelada de TNT
    EARTH_RADIUS = 6371  # km
    
    @staticmethod
    def calculate_mass(diameter_m):
        """
        Calcula la masa de un asteroide esférico
        
        Args:
            diameter_m: Diámetro en metros
        
        Returns:
            Masa en kilogramos
        
        Explicación:
        - Asume asteroide esférico
        - Usa densidad típica de roca (3000 kg/m³)
        - Volumen = (4/3) * π * r³
        - Masa = Volumen × Densidad
        """
        radius_m = diameter_m / 2
        volume_m3 = (4/3) * math.pi * (radius_m ** 3)
        mass_kg = volume_m3 * ImpactPhysics.ASTEROID_DENSITY
        return mass_kg
    
    @staticmethod
    def calculate_kinetic_energy(mass_kg, velocity_km_s):
        """
        Calcula la energía cinética del impacto
        
        Args:
            mass_kg: Masa en kilogramos
            velocity_km_s: Velocidad en km/s
        
        Returns:
            Energía en Joules
        
        Explicación:
        - Energía cinética: E = (1/2) × m × v²
        - Convierte velocidad de km/s a m/s
        """
        velocity_m_s = velocity_km_s * 1000
        energy_joules = 0.5 * mass_kg * (velocity_m_s ** 2)
        return energy_joules
    
    @staticmethod
    def energy_to_tnt_megatons(energy_joules):
        """
        Convierte energía a equivalente en megatones de TNT
        
        Args:
            energy_joules: Energía en Joules
        
        Returns:
            Megatones de TNT
        
        Explicación:
        - 1 tonelada TNT = 4.184 × 10⁹ Joules
        - 1 megatón = 1,000,000 toneladas
        """
        tons_tnt = energy_joules / ImpactPhysics.TNT_JOULES
        megatons_tnt = tons_tnt / 1e6
        return megatons_tnt
    
    @staticmethod
    def calculate_crater_diameter(energy_megatons, target_type='land'):
        """
        Estima el diámetro del cráter
        
        Basado en: Collins et al. (2005) - Earth Impact Effects Program
        
        Args:
            energy_megatons: Energía en megatones TNT
            target_type: 'land' o 'water'
        
        Returns:
            Diámetro del cráter en metros
        
        Explicación:
        - Usa relación de scaling empírica
        - D ≈ 1.8 × (E^0.28) × (ρ_target^-0.33)
        - Tierra tiene mayor densidad que agua
        """
        target_density = 2500 if target_type == 'land' else 1000
        diameter_m = 1.8 * (energy_megatons ** 0.28) * (target_density ** -0.33)
        diameter_m *= 1000  # Convertir a metros
        return diameter_m
    
    @staticmethod
    def calculate_seismic_magnitude(energy_joules):
        """
        Estima la magnitud sísmica (escala Richter)
        
        Basado en: M = 0.67 × log₁₀(E) - 5.87
        
        Args:
            energy_joules: Energía en Joules
        
        Returns:
            Magnitud Richter
        
        Explicación:
        - Relación empírica entre energía y magnitud
        - Similar a cómo se miden terremotos
        """
        if energy_joules <= 0:
            return 0
        
        magnitude = 0.67 * math.log10(energy_joules) - 5.87
        return max(0, magnitude)
    
    @staticmethod
    def calculate_damage_radii(energy_megatons):
        """
        Calcula radios de daño por diferentes efectos
        
        Returns:
            Dict con radios en kilómetros
        
        Explicación:
        - Cada efecto tiene diferente alcance
        - Basado en modelos de armas nucleares (similar física)
        """
        crater_diameter = ImpactPhysics.calculate_crater_diameter(energy_megatons)
        
        return {
            'crater_radius_km': crater_diameter / 2000,
            'fireball_radius_km': 0.5 * (energy_megatons ** 0.4),
            'shockwave_radius_km': 2.0 * (energy_megatons ** 0.33),
            'thermal_radiation_km': 5.0 * (energy_megatons ** 0.4),
            'seismic_effect_km': 50.0 * (energy_megatons ** 0.25)
        }