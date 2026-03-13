from __future__ import annotations

import asyncio
import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse

from audio import validate_audio_file
from database import create_job, get_job, now_iso, update_job

router = APIRouter(prefix="/separate", tags=["separate"])


def _err(code: str, message: str, status: int):
    raise HTTPException(status_code=status, detail={"error": code, "message": message, "details": {}})


@router.post("", status_code=202)
async def post_separate(
    request: Request,
    file: UploadFile = File(...),
    model: str | None = Form(None),
    output_format: str | None = Form(None),
    stems: str | None = Form(None),
):
    app_state = request.app.state
    settings = await app_state.get_settings()
    model = model or settings["model"]
    output_format = output_format or settings["output_format"]
    stem_list = json.loads(stems) if stems else app_state.engine.get_stem_names()

    job_id = str(uuid.uuid4())
    input_path = app_state.config.INPUT_DIR / f"{job_id}_{Path(file.filename).name}"
    input_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open("wb") as f:
        f.write(await file.read())

    meta = validate_audio_file(str(input_path))
    if not meta["valid"]:
        input_path.unlink(missing_ok=True)
        _err("invalid_audio", meta["error"], 400)

    job = {
        "id": job_id,
        "status": "queued",
        "input_filename": file.filename,
        "input_path": str(input_path),
        "output_dir": str(app_state.config.OUTPUT_DIR / job_id),
        "model": model,
        "stems": json.dumps(stem_list),
        "output_format": output_format,
        "sample_rate": settings["sample_rate"],
        "input_duration_seconds": meta["duration_seconds"],
        "input_sample_rate": meta["sample_rate"],
        "input_channels": meta["channels"],
        "input_format": meta["format"],
        "progress_percent": 0,
        "progress_stage": None,
        "created_at": now_iso(),
    }
    await create_job(job)
    app_state.queue.append(job_id)
    app_state.events[job_id] = []
    asyncio.create_task(app_state.process_queue())
    created = await get_job(job_id)
    return {"job": created}


@router.get("/{job_id}")
async def get_separate(job_id: str):
    job = await get_job(job_id)
    if not job:
        _err("job_not_found", "Job not found", 404)
    return {"job": job}


@router.get("/{job_id}/progress")
async def progress(request: Request, job_id: str):
    app_state = request.app.state

    async def event_stream():
        while True:
            if await request.is_disconnected():
                break
            events = app_state.events.get(job_id, [])
            while events:
                item = events.pop(0)
                yield f"event: {item['event']}\ndata: {json.dumps(item['data'])}\n\n"
            await asyncio.sleep(0.4)

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.delete("/{job_id}")
async def cancel_job(request: Request, job_id: str):
    app_state = request.app.state
    job = await get_job(job_id)
    if not job:
        _err("job_not_found", "Job not found", 404)
    if job_id in app_state.queue:
        app_state.queue = [q for q in app_state.queue if q != job_id]
    await update_job(job_id, {"status": "cancelled", "completed_at": now_iso(), "error_message": "Cancelled by user"})
    return {"ok": True}
