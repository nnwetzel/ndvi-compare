from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from ndvi_compare.models.request import ChangeDetectionRequest
from ndvi_compare.services.download import download_image, download_ndvi_difference
import os
import json
import hashlib
from diskcache import Cache

router = APIRouter()
cache = Cache(directory="/tmp/ndvi_cache")

@router.post("/detect_change/")
async def detect_change(request: ChangeDetectionRequest):
    output_dir = os.path.join(os.getcwd(), "maps")
    os.makedirs(output_dir, exist_ok=True)

    # Create a unique hash based on request to avoid overwriting files and use as cache key
    req_data = {"bbox": request.bbox, "date1": request.date1, "date2": request.date2}
    req_hash = hashlib.md5(json.dumps(req_data, sort_keys=True).encode()).hexdigest()

    if req_hash in cache:
        cached_result = cache[req_hash]
        # Check if all files listed in the cache still actually exist on disk
        files_exist = all(
            os.path.exists(os.path.join(output_dir, f)) for f in cached_result["files"]
        )
        
        if files_exist:
            print("Returning cached data")
            cached_result["cached"] = True  # Add this flag so you see it in curl!
            return cached_result
        else:
            print("Cached files missing from disk. Regenerating...")
            del cache[req_hash] # Remove invalid cache entry

    map1_filename = "map_date1.png"
    map2_filename = "map_date2.png"
    diff_filename = "ndvi_diff.png"

    # Download RGB maps
    map1_path = await run_in_threadpool(download_image, request.bbox, request.date1, output_dir, map1_filename)
    map2_path = await run_in_threadpool(download_image, request.bbox, request.date2, output_dir, map2_filename)

    # Generate NDVI difference map
    ndvi_diff_path = await run_in_threadpool(download_ndvi_difference, request.bbox, request.date1, request.date2, output_dir, diff_filename)

    result = {
        "message": "Maps generated successfully.",
        "cached": False,
        "files": [
            os.path.basename(map1_path),
            os.path.basename(map2_path),
            os.path.basename(ndvi_diff_path)
        ]
    }

    # Store result in cache (valid for 30 days)
    cache.set(req_hash, result, expire=2592000)
    
    return result

detect_change_router = router
