# AstroDefender - Backend API

> REST API built with Flask to simulate asteroid impacts and query NASA NeoWs (Near Earth Object Web Service) data.

## 📋 Project Description

This backend project was developed for the **NASA Space Apps Challenge 2024** and provides a complete API that allows:

- 🌍 Query near-Earth asteroids using NASA NeoWs API
- 🔍 Get detailed information about individual asteroids
- 💥 Simulate asteroid impacts with realistic physics calculations
- 📊 Calculate damage zones, seismic magnitudes, and impact effects
- 🗺️ Estimate affected population within different impact radii

---

## 🏗️ Project Architecture

```
Backend/
├── config.py                    # Application configuration (API keys, URLs, CORS)
├── run.py                       # Application entry point
├── requirements.txt             # Project dependencies
├── app/
│   ├── __init__.py             # Factory pattern to create Flask app
│   ├── routes/
│   │   ├── __init__.py         # Main API blueprint
│   │   ├── asteroids.py        # NASA asteroid query endpoints
│   │   └── impact.py           # Impact simulation endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── nasa_service.py     # NASA NeoWs API client
│   │   └── impact_service.py   # Impact simulation logic
│   └── utils/
│       ├── __init__.py
│       └── physics.py          # Physics calculations (mass, energy, crater, etc.)
└── test/
    └── api.http                # HTTP request examples
```

### Main Components

#### 1. **Configuration Layer** (`config.py`)
- Manages environment variables (API keys, external URLs)
- CORS configuration to allow frontend requests
- Rate limiting and environment configuration (development/production)

#### 2. **Application Factory** (`app/__init__.py`)
- Factory pattern to create Flask instances
- Blueprint registration and CORS configuration
- Health check endpoint

#### 3. **Routes Layer** (`app/routes/`)
- **asteroids.py**: Endpoints to query asteroids from NASA
- **impact.py**: Endpoints to simulate impacts

#### 4. **Services Layer** (`app/services/`)
- **nasa_service.py**: NASA NeoWs API integration, data formatting
- **impact_service.py**: Simulation orchestration, impact calculations

#### 5. **Utils Layer** (`app/utils/`)
- **physics.py**: `ImpactPhysics` class with validated scientific formulas

---

## 🚀 API Endpoints

Base URL: `http://localhost:5000/api`

### 1. Asteroid Queries

#### GET `/api/asteroids/near-earth`
Get near-Earth asteroids within a date range.

**Query Parameters:**
- `start_date` (optional): Start date in `YYYY-MM-DD` format
- `end_date` (optional): End date in `YYYY-MM-DD` format

**Example Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "2247517",
      "name": "247517 (2002 QY6)",
      "diameter_min_m": 313.73,
      "diameter_max_m": 701.52,
      "is_potentially_hazardous": false,
      "close_approach_data": [
        {
          "date": "2024-10-05",
          "velocity_km_s": 18.29,
          "miss_distance_km": 28493847.2
        }
      ]
    }
  ]
}
```

#### GET `/api/asteroids/<asteroid_id>`
Get complete details of a specific asteroid.

**Example:** `GET /api/asteroids/2247517`

---

### 2. Impact Simulation

#### POST `/api/impact/simulate`
Simulate asteroid impact with custom parameters.

**Option A - Direct parameters:**
```json
{
  "diameter_m": 250,
  "velocity_km_s": 20,
  "impact_location": {
    "lat": -23.5505,
    "lon": -46.6333
  },
  "target_type": "land"
}
```

**Option B - NASA data:**
```json
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
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "asteroid": {
      "diameter_m": 507.63,
      "mass_kg": 1.72e11,
      "velocity_km_s": 18.29
    },
    "impact": {
      "location": {"lat": -23.5505, "lon": -46.6333},
      "angle_degrees": 45,
      "target_type": "land"
    },
    "energy": {
      "joules": 2.88e18,
      "megatons_tnt": 688.24,
      "hiroshima_bombs": 45883,
      "comparison": "Greater than any nuclear bomb ever tested"
    },
    "crater": {
      "diameter_m": 8947.32,
      "radius_m": 4473.66,
      "comparison": "Approximately 8.9 km diameter - Visible from space"
    },
    "seismic": {
      "magnitude_richter": 6.89,
      "comparison": "Severe damage over wide area"
    },
    "damage_zones": {
      "crater_radius_km": 4.47,
      "fireball_radius_km": 7.23,
      "shockwave_radius_km": 17.59,
      "thermal_radiation_km": 36.15,
      "seismic_effect_km": 257.83
    },
    "population_impact": {
      "method": "simplified_average",
      "estimated_people_affected": 58422,
      "affected_area_km2": 973.7,
      "note": "Estimation using global average density"
    }
  }
}
```

#### POST `/api/impact/simulate-asteroid/<asteroid_id>`
Simulate the impact of a specific NASA asteroid.

**Body:**
```json
{
  "impact_location": {
    "lat": -23.5505,
    "lon": -46.6333
  },
  "target_type": "land"
}
```

**Example:** `POST /api/impact/simulate-asteroid/2247517`

---

### 3. Health Check

#### GET `/health`
Verify that the API is running correctly.

**Response:**
```json
{
  "status": "OK",
  "message": "AstroDefender API is running"
}
```

---

## 🔧 Configuration and Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- NASA API account (optional, uses `DEMO_KEY` by default)

### 1. Install Dependencies

```powershell
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables Configuration

Create a `.env` file in the project root:

```env
# API Keys
NASA_API_KEY=your_api_key_here

# Flask Configuration
FLASK_ENV=development
PORT=5000
SECRET_KEY=your_secret_key_here
```

**Get NASA API Key:**
1. Visit: https://api.nasa.gov/
2. Complete the registration form
3. Copy your API key and add it to the `.env` file

### 3. Run the Application

```powershell
python run.py
```

The API will be available at: `http://localhost:5000`

### 4. Verify Installation

```powershell
# PowerShell
Invoke-WebRequest -Uri http://localhost:5000/health
```

---

## 📦 Dependencies

Listed in `requirements.txt`:

- **Flask** `2.3.2` - Minimalist web framework
- **Flask-CORS** `4.0.0` - Cross-Origin Resource Sharing handler
- **requests** `2.31.0` - HTTP client for consuming external APIs
- **python-dotenv** `1.0.0` - Environment variable management

---

## 🧮 Physics Model and Calculations

### Implemented Formulas (`app/utils/physics.py`)

#### 1. **Mass Calculation**
```python
# Assumes spherical asteroid with rock density (3000 kg/m³)
Volume = (4/3) × π × r³
Mass = Volume × Density
```

#### 2. **Kinetic Energy**
```python
E = (1/2) × m × v²
# Converted to megatons of TNT (1 MT = 4.184 × 10^15 J)
```

#### 3. **Crater Diameter**
Based on **Collins et al. (2005)** - Earth Impact Effects Program:
```python
D ≈ 1.8 × (E^0.28) × (ρ_target^-0.33)
```

#### 4. **Seismic Magnitude (Richter)**
```python
M = 0.67 × log₁₀(E) - 5.87
```

#### 5. **Damage Radii**
- **Crater**: Calculated diameter / 2
- **Fireball**: `0.5 × (E^0.4)` km
- **Shockwave**: `2.0 × (E^0.33)` km
- **Thermal radiation**: `5.0 × (E^0.4)` km
- **Seismic effect**: `50.0 × (E^0.25)` km

### Physical Constants Used
- Typical asteroid density: **3000 kg/m³**
- TNT energy: **4.184 × 10⁹ J/ton**
- Earth radius: **6371 km**

---

## 🔗 Official Documentation Links

### 1. NASA APIs

#### NASA NEO (Near Earth Objects) API
- **Official documentation**: https://api.nasa.gov/
- **NEO-specific guide**: https://api.nasa.gov/ (scroll down → "Asteroids - NeoWs")
- **Request API Key**: https://api.nasa.gov/ (form on the same page)
- **Project GitHub**: https://github.com/nasa/api-docs

#### NASA JPL Small-Body Database
- **Lookup tool**: https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html
- **API Browser**: https://ssd-api.jpl.nasa.gov/doc/sbdb.html
- **Orbital elements documentation**: https://ssd.jpl.nasa.gov/planets/approx_pos.html

#### NASA Eyes on Asteroids
- **3D Visualization**: https://eyes.nasa.gov/apps/asteroids/#/home
- **Documentation**: https://eyes.nasa.gov/

---

### 2. Distance Matrix AI

#### Geocoding API
- **Main page**: https://distancematrix.ai/
- **Geocoding documentation**: https://distancematrix.ai/dev/docs/geocoding
- **Dashboard (for API key)**: https://distancematrix.ai/dashboard
- **Pricing and limits**: https://distancematrix.ai/pricing

---

### 3. OpenStreetMap - Overpass API

#### Overpass API
- **Official documentation**: https://wiki.openstreetmap.org/wiki/Overpass_API
- **Overpass Turbo (testing)**: https://overpass-turbo.eu/
- **Overpass QL language guide**: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL
- **Query examples**: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_API_by_Example

#### Nominatim (geocoding alternative)
- **Documentation**: https://nominatim.org/release-docs/latest/
- **API reference**: https://nominatim.org/release-docs/latest/api/Overview/
- **Usage policies**: https://operations.osmfoundation.org/policies/nominatim/

---

### 4. USGS APIs

#### USGS Earthquake Catalog
- **API Documentation**: https://earthquake.usgs.gov/fdsnws/event/1/
- **Web Service**: https://earthquake.usgs.gov/fdsnws/event/1/query
- **Parameters and examples**: https://earthquake.usgs.gov/fdsnws/event/1/#parameters

#### USGS National Map - Elevation Data
- **Main page**: https://www.usgs.gov/programs/national-geospatial-program/national-map
- **Elevation Products**: https://www.usgs.gov/3d-elevation-program
- **TNM API**: https://apps.nationalmap.gov/tnmaccess/#/
- **Training videos**: https://www.usgs.gov/media/videos/national-map-training-videos

---

### 5. Scientific Documentation

#### Impact Formulas
- **Earth Impact Effects Program**: https://impact.ese.ic.ac.uk/ImpactEarth/ImpactEffects/
- **Collins et al. (2005) Paper**: https://www.lpi.usra.edu/meetings/lpsc2005/pdf/1981.pdf
- **NASA Impact Risk Assessment**: https://cneos.jpl.nasa.gov/sentry/

#### Orbital Mechanics
- **Keplerian Elements**: https://solarsystem.nasa.gov/basics/chapter4-1/
- **JPL Horizons System**: https://ssd.jpl.nasa.gov/horizons/
- **Orbital Mechanics Tutorial**: https://www.braeunig.us/space/orbmech.htm

---

### 6. Python Frameworks and Libraries

#### Flask
- **Official documentation**: https://flask.palletsprojects.com/
- **Quickstart**: https://flask.palletsprojects.com/en/3.0.x/quickstart/
- **Flask-CORS**: https://flask-cors.readthedocs.io/

#### Requests
- **Documentation**: https://requests.readthedocs.io/
- **Quickstart**: https://requests.readthedocs.io/en/latest/user/quickstart/

#### NumPy & SciPy (if project is expanded)
- **NumPy**: https://numpy.org/doc/
- **SciPy**: https://docs.scipy.org/doc/scipy/

---

### 7. NASA Space Apps Hackathon Resources

#### Specific Challenge
- **Challenge page**: https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/
- **Provided resources**: Search for "Asteroid Impact Simulation" on the challenge page

#### Additional Datasets
- **NASA Open Data Portal**: https://data.nasa.gov/
- **USGS EarthExplorer**: https://earthexplorer.usgs.gov/
- **Canadian Space Agency - NEOSSat**: https://www.asc-csa.gc.ca/eng/satellites/neossat/

---

### 8. Standards and Formats

#### GeoJSON
- **Specification**: https://geojson.org/
- **RFC 7946**: https://tools.ietf.org/html/rfc7946

#### ISO 8601 (Dates)
- **Standard**: https://en.wikipedia.org/wiki/ISO_8601

---

## 📚 References for Citation

1. NASA Near Earth Object Web Service (NeoWs) API. NASA/JPL. https://api.nasa.gov/
2. Distance Matrix AI Geocoding API. https://distancematrix.ai/dev/docs/geocoding
3. Overpass API. OpenStreetMap Foundation. https://wiki.openstreetmap.org/wiki/Overpass_API
4. USGS Earthquake Hazards Program - Web Services. https://earthquake.usgs.gov/fdsnws/event/1/
5. Collins, G.S., Melosh, H.J., Marcus, R.A. (2005). Earth Impact Effects Program. https://impact.ese.ic.ac.uk/
6. JPL Small-Body Database. NASA/JPL. https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html

---

## 🧪 Testing

### Request Examples with PowerShell

```powershell
# 1. Health check
Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET

# 2. Get near-Earth asteroids
Invoke-RestMethod -Uri "http://localhost:5000/api/asteroids/near-earth?start_date=2024-10-01&end_date=2024-10-07" -Method GET

# 3. Simulate impact
$body = @{
    diameter_m = 250
    velocity_km_s = 20
    impact_location = @{
        lat = -23.5505
        lon = -46.6333
    }
    target_type = "land"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/impact/simulate" -Method POST -Body $body -ContentType "application/json"
```

---

## 🚧 Next Steps and Recommended Improvements

### Pending Features
- [ ] Implement unit tests with `pytest`
- [ ] Add WorldPop API integration for precise population estimates
- [ ] Implement NASA response caching (Redis)
- [ ] Add rate limiting per IP
- [ ] Create endpoint for impact zone visualization (GeoJSON)
- [ ] Dockerize the application
- [ ] CI/CD with GitHub Actions

### Code Improvements
- [ ] Add schema validation with `marshmallow` or `pydantic`
- [ ] Implement structured logging
- [ ] Add metrics and observability (Prometheus)
- [ ] OpenAPI/Swagger documentation

### Deployment
- [ ] Prepare for Azure App Service
- [ ] Configure environment variables in production
- [ ] Implement HTTPS and SSL certificates
- [ ] Configure custom domain

---

## 👥 Team - Locura de Meteoritos

Developed for the **NASA Space Apps Challenge 2024**.

---

## 📄 License

This project is open source and available under the license terms determined by the team.

---

## 🆘 Support

For questions or issues:
1. Review the external API documentation
2. Check the application logs
3. Contact the development team

---

**Thank you for using AstroDefender! 🌍💫**
