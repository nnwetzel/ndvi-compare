from pydantic import BaseModel
from typing import List

class ChangeDetectionRequest(BaseModel):
    bbox: List[float]  # [min, lon, min_lat, max_lon, max_lat]
    date1: str         # ISO format date string
    date2: str         # ISO format date string

class NDVIDifferenceRequest(BaseModel):
    bbox: List[float]  # [min_lon, min_lat, max_lon, max_lat]
    date1: str         # ISO format date string
    date2: str         # ISO format date string
    filename: str = "ndvi_diff.png"  # Default filename for the output image