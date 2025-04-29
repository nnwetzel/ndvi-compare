from fastapi import FastAPI
from geochange_detection_api.api.endpoints import detect_change_router
from geochange_detection_api.util.config import get_config
import uvicorn
import ee

app = FastAPI()

# Initialize Earth Engine
service_account = get_config().GEE_PROJECT_ID
credentials_path = get_config().GEE_CREDENTIALS

credentials = ee.ServiceAccountCredentials(service_account, credentials_path)
ee.Initialize(credentials)

# Attach routers
app.include_router(detect_change_router)

@app.get("/")
def root():
    return {"message": "GeoChange Detection API Ready"}

def main():
    uvicorn.run("geochange_detection_api.main:app", host=get_config().HOST, port=get_config().PORT, reload=True)

if __name__ == "__main__":
    main()
