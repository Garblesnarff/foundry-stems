from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from database import delete_history, delete_job, get_job, history, stats

router = APIRouter(prefix="/history", tags=["history"])


@router.get("")
async def get_history(search: str = "", sort: str = "newest", limit: int = 50, offset: int = 0):
    jobs, total = await history(search=search, sort=sort, limit=limit, offset=offset)
    return {"jobs": jobs, "total": total, "limit": limit, "offset": offset}


@router.get("/stats")
async def get_stats():
    return await stats()


@router.delete("/{job_id}")
async def remove_history_item(job_id: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "job_not_found", "message": "Job not found", "details": {}})
    for stem in job.get("stem_files", []):
        Path(stem["output_path"]).unlink(missing_ok=True)
    Path(job["input_path"]).unlink(missing_ok=True)
    if job.get("output_dir"):
        shutil.rmtree(job["output_dir"], ignore_errors=True)
    await delete_job(job_id)
    return {"ok": True}


@router.delete("")
async def clear_history():
    await delete_history()
    return {"ok": True}
