# Satellite Change Detection Service
FastAPI backend for detecting changes between satellite imagery using Google Earth Engine.

## Prerequisites
- Install uv
- Install Python 3.11 or 3.12
- Register for Google Earth Engine access: [Google Earth Engine Registration](https://signup.earthengine.google.com/)
- Set up a Google Cloud Project (automatically created after Earth Engine signup)

Setup
1. Bootstrap the environment (creates .venv, installs dependencies):
```bash
make bootstrap
```

2. Activate the virtual environment:
```bash
source .venv/bin/activate
```

3. Authenticate with Earth Engine:
```bash
earthengine authenticate
```

4. Set your Earth Engine Project ID

Create a .env file in the root of the project:
```bash
touch .env
```

Add the following line to .env:
```bash
GEE_PROJECT_ID=your-google-cloud-project-id
```

(Replace your-google-cloud-project-id with your actual Google Cloud Project ID, like commanding-way-458301-u7.)

## Running Locally
Start the application:
```bash
make run
```

The server will start on:

http://127.0.0.1:8000

Mato Grosso, Brazil (Amazon deforestation)
```bash
curl -X POST http://127.0.0.1:8000/detect_change/ \
  -H "Content-Type: application/json" \
  -d '{
        "bbox": [-55.5, -12.5, -54.5, -11.5],
        "date1": "2019-06-01",
        "date2": "2024-06-01"
      }'
```

Las Vegas Urban Growth (City expansion into desert)

```bash
curl -X POST http://127.0.0.1:8000/detect_change/ \
  -H "Content-Type: application/json" \
  -d '{
        "bbox": [-115.39, 35.96, -114.90, 36.36],
        "date1": "2016-06-01",
        "date2": "2024-06-01"
      }'
```

Paradise, California, USA (Wildfire destruction and slow regrowth)

```bash
curl -X POST http://127.0.0.1:8000/detect_change/ \
  -H "Content-Type: application/json" \
  -d '{
        "bbox": [-121.65, 39.73, -121.55, 39.83],
        "date1": "2019-06-01",
        "date2": "2024-06-01"
      }'
```

This will download ```.png``` files containing real satellite imagery for both dates.

## Notes
- Users must authenticate with their own Google Earth Engine account.
- Users must have a Google Cloud project ID tied to their Earth Engine access.
- The ```.env``` file is used to securely load your project ID without hardcoding.
- Images are retrieved at 512px resolution in true color (RGB bands: B4, B3, B2).
