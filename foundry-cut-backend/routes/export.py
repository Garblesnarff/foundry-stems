from __future__ import annotations

import shutil
import uuid
import zipfile
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from audio import convert_audio
from database import get_job
from models import ExportBatchRequest, ExportStemRequest

router = APIRouter(prefix="/export", tags=["export"])


@router.post("/stems")
async def export_stems(payload: ExportStemRequest):
    job = await get_job(payload.job_id)
    if not job:
        raise HTTPException(status_code=404, detail={"error": "job_not_found", "message": "Job not found", "details": {}})
    selected = [s for s in job.get("stem_files", []) if s["name"] in payload.stems]
    if payload.mode == "individual":
        if len(selected) != 1:
            raise HTTPException(status_code=400, detail="Individual mode requires exactly one stem")
        stem = selected[0]
        src = Path(stem["output_path"])
        out = src
        if src.suffix.lstrip(".") != payload.format:
            out = src.with_suffix(f".{payload.format}")
            convert_audio(str(src), str(out), payload.format)
        return FileResponse(out, filename=out.name)

    zip_path = Path(job["output_dir"]) / f"export_{uuid.uuid4().hex[:8]}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for stem in selected:
            src = Path(stem["output_path"])
            write_path = src
            if src.suffix.lstrip(".") != payload.format:
                write_path = src.with_suffix(f".{payload.format}")
                convert_audio(str(src), str(write_path), payload.format)
            zf.write(write_path, arcname=write_path.name)
    return FileResponse(zip_path, filename=zip_path.name)


@router.post("/batch")
async def export_batch(payload: ExportBatchRequest):
    batch_zip = Path("/tmp") / f"foundry_cut_batch_{uuid.uuid4().hex[:8]}.zip"
    with zipfile.ZipFile(batch_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in payload.jobs:
            job = await get_job(item.job_id)
            if not job:
                continue
            for stem in [s for s in job.get("stem_files", []) if s["name"] in item.stems]:
                src = Path(stem["output_path"])
                converted = src
                if src.suffix.lstrip(".") != payload.format:
                    converted = src.with_suffix(f".{payload.format}")
                    convert_audio(str(src), str(converted), payload.format)
                zf.write(converted, arcname=f"{Path(job['input_filename']).stem}/{converted.name}")
    return FileResponse(batch_zip, filename=batch_zip.name)
