# Mobile Network Coverage API (France)

This project provides a REST API to retrieve **mobile network coverage (2G/3G/4G)** by operator for a given address in metropolitan France.

The API combines:

- **French official geocoding API** ([adresse.data.gouv.fr](https://adresse.data.gouv.fr/api)) to resolve textual addresses.
- **Mobile network coverage dataset** per city and operator (preprocessed from points provided by the test).  
- **City-level coverage mapping** via spatial join with official French commune boundaries.

---

## Features

- Returns network coverage for all major French operators:
  - Orange
  - SFR
  - Bouygues
  - Free
- Coverage per operator (`2G`, `3G`, `4G`) at **city-level precision**
- Includes **confidence score** (which is not officially documented, or not found in the documentation, but still provided by the API, so there is not a 100% certainty it is indeed a confidence score, it is provided just as "score" in the response) from the geocoding API, and the **matched city** so the user will know which city was matched by the API.
- Fully **Dockerized** for easy deployment
- Handles invalid addresses with clear error responses

---

## API Usage

### Endpoint

```
GET /api/coverage/?address=<TEXTUAL_ADDRESS>
```

### Example

**Request:**

```
GET /api/coverage/?address=42+rue+papernest+75011+Paris
```

**Response: (example)**

```json
{
  "matched_city": "Paris",
  "confidence_score": 0.95,
  "coverage": {
    "Orange": {"2G": true, "3G": true, "4G": true},
    "SFR": {"2G": true, "3G": true, "4G": false},
    "Bouygues": {"2G": true, "3G": true, "4G": true},
    "Free": {"2G": false, "3G": true, "4G": true}
  }
}
```

## Data Source

* Original points (Lambert93): provided by the technical test. Contains operator IDs and 2G/3G/4G coverage.

* Official French communes: communes.gpkg (used to map points to official city names). (directly downloadable on
https://drive.google.com/file/d/137n6Phm9lt4mON5lWEeUL7xeES-MLxNy/view?usp=sharing as it is in a zip file in https://geoservices.ign.fr/telechargement-api/ADMIN-EXPRESS)

### Preprocessing Workflow

The raw points in Lambert93 (EPSG:2154) were converted to WGS84 coordinates (lat/lon), then spatially joined with official French communes polygons to assign each point to a city. Only one record per city/operator combination was kept.

## Installation
Using Docker

```
docker-compose up --build
```

API will be available at http://localhost:8000/api/coverage/

There is also an UI with swagger to test the API easier, via http://localhost:8000/swagger/


Without Docker

```
Create a virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## Known limitations
* Coverage is city-level only, not street-level.

* Dataset from 2018; real coverage may differ.

* Geocoding confidence score is provided by the API, not formally documented.

* Depends on external geocoding service availability.
