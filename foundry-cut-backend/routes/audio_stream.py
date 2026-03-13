from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from audio import get_audio_waveform_data
from database import get_job

router = APIRouter(prefix="/audio", tags=["audio"])


@router.get("/{job_id}/{stem_name}")
async def stream_audio(job_id: str, stem_name: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "job_not_found", "message": "Job not found", "details": {}})
    if stem_name == "original":
        path = Path(job["input_path"])
    else:
        stem = next((s for s in job.get("stem_files", []) if s["name"] == stem_name), None)
        if not stem:
            raise HTTPException(status_code=404, detail="Stem not found")
        path = Path(stem["output_path"])
    return FileResponse(path, headers={"Accept-Ranges": "bytes"})


@router.get("/{job_id}/{stem_name}/waveform")
async def waveform(job_id: str, stem_name: str):
    job = await get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "job_not_found", "message": "Job not found", "details": {}})
    if stem_name == "original":
        path = job["input_path"]
    else:
        stem = next((s for s in job.get("stem_files", []) if s["name"] == stem_name), None)
        if not stem:
            raise HTTPException(status_code=404, detail="Stem not found")
        path = stem["output_path"]
    points = get_audio_waveform_data(path)
    return {"stem": stem_name, "points": points, "duration_seconds": job.get("input_duration_seconds", 0), "num_points": len(points)}
