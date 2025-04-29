import os
import ee
import uvicorn
import requests
import datetime
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import box

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import List

from .util.config import get_config

app = FastAPI()

# Initialize Earth Engine
ee.Initialize(project=get_config().GEE_PROJECT_ID)

class ChangeDetectionRequest(BaseModel):
    bbox: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    date1: str         # ISO format date string
    date2: str         # ISO format date string

def download_image(bbox: List[float], date: str, output_dir: str, filename: str) -> str:
    min_lon, min_lat, max_lon, max_lat = bbox
    geom = ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")

    # Choose wider or tighter date window
    delta_days = 30 if date_obj < datetime.datetime(2015, 6, 23) else 10
    start_date = (date_obj - datetime.timedelta(days=delta_days)).strftime("%Y-%m-%d")
    end_date = (date_obj + datetime.timedelta(days=delta_days)).strftime("%Y-%m-%d")

    # Pick dataset and bands
    if date_obj >= datetime.datetime(2017, 3, 1):
        collection_id, bands = 'COPERNICUS/S2_SR_HARMONIZED', ['B4', 'B3', 'B2']
    elif date_obj >= datetime.datetime(2015, 6, 23):
        collection_id, bands = 'COPERNICUS/S2_HARMONIZED', ['B4', 'B3', 'B2']
    else:
        collection_id, bands = 'LANDSAT/LC08/C02/T1_L2', ['SR_B4', 'SR_B3', 'SR_B2']

    cloud_thresh = 70 if collection_id.startswith('LANDSAT') else 20

    collection = ee.ImageCollection(collection_id) \
        .filterBounds(geom) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_thresh))

    if collection.size().getInfo() == 0:

        raise HTTPException(status_code=404, detail=f"No imagery available for {date} at this location between {start_date} and {end_date}.")


    mosaic = collection.mosaic().clip(geom)

    url = mosaic.getThumbURL({
        'region': geom,
        'dimensions': 1024,
        'format': 'png',
        'bands': bands,
        'min': 0,
        'max': 3000
    })

    output_path = os.path.join(output_dir, filename)
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

    return output_path

@app.post("/detect_change/")
async def detect_change(request: ChangeDetectionRequest):
    output_dir = os.path.join(os.getcwd(), "maps")
    os.makedirs(output_dir, exist_ok=True)

    map1_path = await run_in_threadpool(download_image, request.bbox, request.date1, output_dir, "map_date1.png")
    map2_path = await run_in_threadpool(download_image, request.bbox, request.date2, output_dir, "map_date2.png")

    return {"message": "Maps generated successfully.", "files": ["map_date1.png", "map_date2.png"]}

@app.get("/")
def root():
    return {"message": "Satellite Change Detection API Ready"}

def main():
    uvicorn.run("satellite_change_service.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
