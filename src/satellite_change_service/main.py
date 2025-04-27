from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_origin
import tempfile
import os
from fastapi.responses import FileResponse

app = FastAPI()

class ChangeDetectionRequest(BaseModel):
    bbox: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    date1: str         # ISO format date string
    date2: str

@app.post("/detect_change/")
def detect_change(request: ChangeDetectionRequest):
    # --- For now, create dummy NDVI images instead of real satellite download ---

    width, height = 256, 256  # Small test image

    # Simulate two NDVI arrays
    np.random.seed(42)
    ndvi_1 = np.random.uniform(0.2, 0.8, (height, width))
    ndvi_2 = ndvi_1 + np.random.normal(0, 0.1, (height, width))  # Small change

    # Compute NDVI difference
    delta_ndvi = ndvi_2 - ndvi_1

    # Create binary change map: -0.2 threshold for loss
    change_map = np.where(delta_ndvi < -0.2, 1, 0).astype(rasterio.uint8)

    # Create a dummy GeoTIFF to return
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "change_map.tif")

    transform = from_origin(request.bbox[0], request.bbox[3], 0.0001, 0.0001)
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=change_map.shape[0],
        width=change_map.shape[1],
        count=1,
        dtype=rasterio.uint8,
        crs='EPSG:4326',
        transform=transform,
    ) as dst:
        dst.write(change_map, 1)

    return FileResponse(output_path, media_type="image/tiff", filename="change_map.tif")

@app.get("/")
def root():
    return {"message": "Satellite Change Detection API Ready"}

def main():
    import uvicorn
    uvicorn.run("satellite_change_service.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()