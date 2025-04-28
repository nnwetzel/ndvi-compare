import matplotlib
# Set the backend to Agg to avoid GUI issues
matplotlib.use('Agg')

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import numpy as np
import rasterio
from rasterio.transform import from_origin
import tempfile
import os
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import contextily as ctx  # <-- NEW
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

class ChangeDetectionRequest(BaseModel):
    bbox: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    date1: str         # ISO format date string
    date2: str         # ISO format date string

@app.post("/detect_change/")
def detect_change(request: ChangeDetectionRequest):
    # Coordinates from the request
    min_lon, min_lat, max_lon, max_lat = request.bbox

    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot an empty scatter just to initialize correct bounds
    ax.set_xlim(min_lon, max_lon)
    ax.set_ylim(min_lat, max_lat)

    # Add basemap (real world imagery) using contextily
    # contextily expects Web Mercator (EPSG:3857), so we need to reproject
    import geopandas as gpd
    from shapely.geometry import box

    geom = box(min_lon, min_lat, max_lon, max_lat)
    gdf = gpd.GeoDataFrame(geometry=[geom], crs="EPSG:4326")  # WGS84
    gdf = gdf.to_crs(epsg=3857)  # Reproject to Web Mercator

    ax.set_xlim(gdf.total_bounds[[0, 2]])
    ax.set_ylim(gdf.total_bounds[[1, 3]])

    ctx.add_basemap(ax, crs=gdf.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)  # Or ctx.providers.OpenStreetMap.Mapnik

    # Draw the bounding box itself
    gdf.boundary.plot(ax=ax, edgecolor='red', linewidth=2)

    ax.set_title("Bounding Box on Real-World Map")

    # Save the figure as a PNG file
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "bounding_box_map.png")
    fig.savefig(output_path, bbox_inches='tight')

    # Return the image file as a response
    return FileResponse(output_path, media_type="image/png", filename="bounding_box_map.png")

@app.get("/")
def root():
    return {"message": "Satellite Change Detection API Ready"}

def main():
    import uvicorn
    uvicorn.run("satellite_change_service.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()