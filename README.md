# GeoChange Detection API 
FastAPI backend for detecting changes between satellite imagery using Google Earth Engine (GEE).

## Prerequisites
**1. uv**

Install from:
https://docs.astral.sh/uv/getting-started/installation/

**2. Python 3.11**

Install using:
```bash
uv python install 3.11
```

**3. Google Earth Engine access**
- Register for access:
https://signup.earthengine.google.com/
- During signup, select noncommercial use unless you are working on a commercial application.
- After approval, create a Google Cloud Project linked to your Earth Engine account at:
https://console.cloud.google.com/cloud-resource-manager

**4. Google Cloud Project with Earth Engine API enabled**
- Enable the Earth Engine API here:
https://console.cloud.google.com/apis/library/earthengine.googleapis.com
- Make sure the correct project is selected when enabling the API.

## Local Setup
**1. Bootstrap environment**
```bash
make bootstrap
```

**2. Activate virtual environment**
```bash#
source .venv/bin/activate
```

**3. Authenticate Earth Engine (for local dev)**
```bash
earthengine authenticate
```

**4. Create a ```.env``` file in the root directory**

Create the file:
```bash
touch .env
```

Edit it:
```bash
nano .env
```

Find your Google Cloud Project ID here:
https://console.cloud.google.com/cloud-resource-manager

Then paste the following into ```.env```, updating ```your-google-cloud-project-id```:
```bash
GEE_PROJECT_ID=your-google-cloud-project-id
GEE_CREDENTIALS=secrets/earthengine-privatekey.json
```

## Running Locally
Start the API server:
```bash
make run
```

Visit:
http://127.0.0.1:8000

## Docker Usage
**1. Build the image**
```bash
docker build -t geochange-detection-api .
```

**2. Create a ```.env``` file in the root directory**

Create the file:
```bash
touch .env
```

Edit it:
```bash
nano .env
```

Find your Google Cloud Project ID here:
https://console.cloud.google.com/cloud-resource-manager

Then paste the following into .env, updating ```your-google-cloud-project-id```:
```bash
GEE_PROJECT_ID=your-google-cloud-project-id
GEE_CREDENTIALS=/app/secrets/earthengine-privatekey.json
```

**3. Add your credentials**

To complete this set:

[How to Generate earthengine-privatekey.son](https://github.com/nnwetzel/geochange-detection-api?tab=readme-ov-file#how-to-generate-earthengine-privatekeyjson)

Place your downloaded Earth Engine service account key at:
```secrets/earthengine-privatekey.json```

**4. Run the container**
```bash
make docker-run
```

## How to Generate ```earthengine-privatekey.json```

**Step 1: Create a Service Account**

Go to:
https://console.cloud.google.com/iam-admin/serviceaccounts
- Select your project (the one linked to Earth Engine)
- Click **Create Service Account**
- Service account name: ```earthengine-access```
- Click **Create and Continue**
- Click **Select a role → choose Viewer**
- Click **Done**

**Step 2: Download the Service Account Key**

Still on:
https://console.cloud.google.com/iam-admin/serviceaccounts
- Select your project
- Find your service account (earthengine-access)
- Click the **⋮ (three dots) → Manage keys**
- Click **Add Key → Create new key → select JSON**
- Save the file as: ```secrets/earthengine-privatekey.json```

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
