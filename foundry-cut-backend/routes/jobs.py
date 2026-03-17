from __future__ import annotations

import asyncio
import json
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile

from audio import validate_audio_file
from config import SUPPORTED_MODELS, SUPPORTED_OUTPUT_FORMATS
from database import create_job, list_jobs, now_iso, update_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _err(code: str, message: str, status: int):
    raise HTTPException(status_code=status, detail={"error": code, "message": message, "details": {}})


@router.get("")
async def get_jobs(request: Request):
    processing = [j for j in await list_jobs() if j["status"] == "processing"]
    queued = [j for j in await list_jobs() if j["status"] == "queued"]
    for i, q in enumerate(queued, 1):
        q["position"] = i
    return {"processing": processing[0] if processing else None, "queued": queued}


@router.post("/batch", status_code=202)
async def batch_jobs(
    request: Request,
    files: list[UploadFile] = File(...),
    model: str | None = Form(None),
    output_format: str | None = Form(None),
):
    app_state = request.app.state
    settings = await app_state.get_settings()
    model = model or settings["model"]
    output_format = output_format or settings["output_format"]

    if model not in SUPPORTED_MODELS:
        _err("invalid_setting", f"Unsupported model: {model}", 400)
    if output_format not in SUPPORTED_OUTPUT_FORMATS:
        _err("invalid_setting", f"Unsupported output format: {output_format}", 400)

    jobs = []
    for file in files:
        job_id = str(uuid.uuid4())
        input_path = app_state.config.INPUT_DIR / f"{job_id}_{Path(file.filename).name}"
        with input_path.open("wb") as f:
            f.write(await file.read())
        meta = validate_audio_file(str(input_path))
        if not meta["valid"]:
            input_path.unlink(missing_ok=True)
            continue
        job = {
            "id": job_id,
            "status": "queued",
            "input_filename": file.filename,
            "input_path": str(input_path),
            "output_dir": str(app_state.config.OUTPUT_DIR / job_id),
            "model": model,
            "stems": json.dumps(["vocals", "drums", "bass", "other"]),
            "output_format": output_format,
            "sample_rate": settings["sample_rate"],
            "input_duration_seconds": meta["duration_seconds"],
            "input_sample_rate": meta["sample_rate"],
            "input_channels": meta["channels"],
            "input_format": meta["format"],
            "progress_percent": 0,
            "created_at": now_iso(),
        }
        await create_job(job)
        app_state.queue.append(job_id)
        jobs.append(job)
    asyncio.create_task(app_state.process_queue())
    return {"jobs": jobs}


@router.delete("/queue")
async def clear_queue(request: Request):
    app_state = request.app.state
    queue = app_state.queue[:]
    app_state.queue.clear()
    for job_id in queue:
        await update_job(job_id, {"status": "cancelled", "completed_at": now_iso(), "error_message": "Cleared from queue"})
    return {"cleared": len(queue)}
