# GeoChange Detection API
FastAPI backend for detecting changes between satellite imagery using Google Earth Engine (GEE).

## Prerequisites
- Python 3.11 or 3.12
- uv package manager
- Google Earth Engine access
- A Google Cloud Project with the Earth Engine API enabled

# Local Setup
1. Bootstrap environment
```bash
make bootstrap
```

2. Activate virtual environment
```bash
source .venv/bin/activate
```

3. Authenticate Earth Engine (for local dev)
```bash
earthengine authenticate
```

4. Create a ```.env``` file in the root directory
```bash
touch .env
nano .env
```

Paste the following and update the placeholders:
```bash
GEE_PROJECT_ID=your-google-cloud-project-id
```

# Running Locally
Start the API server:
```bash
make run
```

Visit:
http://127.0.0.1:8000

## Docker Usage
1. Build the image
```bash
docker build -t geochange-detection-api .
```

2. Update ```.env```

Paste the following and update the placeholders:

```bash
GEE_PROJECT_ID=your-google-cloud-project-id
GEE_CREDENTIALS=/app/secrets/earthengine-privatekey.json
```

3. Add your credentials
Place your downloaded Earth Engine service account key at:
secrets/earthengine-privatekey.json

4. Run the container
```bash
make docker-run
```

## How to Generate earthengine-privatekey.json
Step 1: Enable the Earth Engine API
https://console.cloud.google.com/apis/library/earthengine.googleapis.com

Step 2: Create a Service Account
https://console.cloud.google.com/iam-admin/serviceaccounts

- Click **Create Service Account**
- Service account name: ```earthengine-access```
- Click **Create and Continue**
- Role: **Select a role: Viewer**
- Click **Done**

Step 3: Download the Key
- Click on the 3 dots (of the service account you just created)
- Click **Manage Key → Add Key → Create new key → JSON**
- Save it as ```secrets/earthengine-privatekey.json```

## Example API Usage
Amazon Deforestation (Mato Grosso)
```bash
curl -X POST http://localhost:8000/detect_change/ \
-H "Content-Type: application/json" \
-d '{
"bbox": [-55.5, -12.5, -54.5, -11.5],
"date1": "2019-06-01",
"date2": "2024-06-01"
}'
```

Las Vegas Urban Growth
```bash
curl -X POST http://localhost:8000/detect_change/ \
-H "Content-Type: application/json" \
-d '{
"bbox": [-115.39, 35.96, -114.90, 36.36],
"date1": "2016-06-01",
"date2": "2024-06-01"
}'
```

Paradise, CA Wildfire Recovery
```bash
curl -X POST http://localhost:8000/detect_change/ \
-H "Content-Type: application/json" \
-d '{
"bbox": [-121.65, 39.73, -121.55, 39.83],
"date1": "2019-06-01",
"date2": "2024-06-01"
}'
```
