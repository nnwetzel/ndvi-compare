from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from geochange_detection_api.models.request import ChangeDetectionRequest
from geochange_detection_api.services.download import download_image
import os

router = APIRouter()

@router.post("/detect_change/")
async def detect_change(request: ChangeDetectionRequest):
    output_dir = os.path.join(os.getcwd(), "maps")
    os.makedirs(output_dir, exist_ok=True)
    
    map1_path = await run_in_threadpool(download_image, request.bbox, request.date1, output_dir, "map_date1.png")
    map2_path = await run_in_threadpool(download_image, request.bbox, request.date2, output_dir, "map_date2.png")

    return {"message": "Maps generated successfully.", "files": ["map_date1.png", "map_date2.png"]}

detect_change_router = router