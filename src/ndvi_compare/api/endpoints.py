from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from ndvi_compare.models.request import ChangeDetectionRequest
from ndvi_compare.services.download import download_image, download_ndvi_difference
import os

router = APIRouter()

@router.post("/detect_change/")
async def detect_change(request: ChangeDetectionRequest):
    output_dir = os.path.join(os.getcwd(), "maps")
    os.makedirs(output_dir, exist_ok=True)

    # Download RGB maps
    map1_path = await run_in_threadpool(download_image, request.bbox, request.date1, output_dir, "map_date1.png")
    map2_path = await run_in_threadpool(download_image, request.bbox, request.date2, output_dir, "map_date2.png")

    # Generate NDVI difference map
    ndvi_diff_path = await run_in_threadpool(download_ndvi_difference, request.bbox, request.date1, request.date2, output_dir, "ndvi_diff.png")

    return {
        "message": "Maps generated successfully.",
        "files": [
            os.path.basename(map1_path),
            os.path.basename(map2_path),
            os.path.basename(ndvi_diff_path)
        ]
    }

detect_change_router = router
