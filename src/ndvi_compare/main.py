from fastapi import FastAPI
from ndvi_compare.api.endpoints import detect_change_router
from ndvi_compare.util.config import get_config
from ndvi_compare.services.download import download_ndvi_difference
from typing import List
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
    return {"message": "NDVI Compare Ready"}

@app.get("/health")
def health_check():
    try:
        ee.Initialize()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

def main():
    uvicorn.run("ndvi_compare.main:app", host=get_config().HOST, port=get_config().PORT, reload=True)

if __name__ == "__main__":
    main()
