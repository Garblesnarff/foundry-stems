from __future__ import annotations

import asyncio
import json
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from audio import save_stem
from database import add_stem, fetch_settings, get_job, init_db, now_iso, update_job
from engine import DemucsEngine
from routes import audio_stream, export, health, history, jobs, separate, settings


class AppState:
    def __init__(self):
        self.config = config
        self.engine = DemucsEngine(model_name=config.DEFAULT_MODEL, num_threads=config.DEFAULT_NUM_THREADS)
        self.queue: list[str] = []
        self.events: dict[str, list[dict]] = {}
        self._processing_task_lock = asyncio.Lock()

    async def get_settings(self):
        return await fetch_settings()

    def emit(self, job_id: str, event: str, data: dict):
        self.events.setdefault(job_id, []).append({"event": event, "data": data})

    async def process_queue(self):
        if self._processing_task_lock.locked():
            return
        async with self._processing_task_lock:
            while self.queue:
                if self.engine.processing:
                    await asyncio.sleep(0.1)
                    continue
                job_id = self.queue.pop(0)
                job = await get_job(job_id)
                if not job or job["status"] in {"cancelled", "failed"}:
                    continue
                try:
                    await update_job(job_id, {"status": "processing", "started_at": now_iso(), "progress_stage": "analyzing", "progress_percent": 1})
                    self.emit(job_id, "progress", {"stage": "analyzing", "percent": 1})

                    if job["model"] != self.engine.model_name:
                        await self.engine.switch_model(job["model"])

                    def on_progress(payload: dict):
                        asyncio.create_task(update_job(job_id, {"progress_stage": payload["stage"], "progress_percent": payload["percent"]}))
                        self.emit(job_id, "progress", payload)

                    result = await self.engine.separate(job["input_path"], job_id, progress_callback=on_progress)
                    output_dir = Path(job["output_dir"])
                    output_dir.mkdir(parents=True, exist_ok=True)
                    for stem_name, tensor in result["stems"].items():
                        if stem_name not in job["stems"]:
                            continue
                        stem_path = output_dir / f"{stem_name}.{job['output_format']}"
                        saved = save_stem(
                            waveform=tensor.cpu(),
                            sample_rate=result["sample_rate"],
                            output_path=str(stem_path),
                            format=job["output_format"],
                            target_sample_rate=job["sample_rate"],
                        )
                        await add_stem(
                            {
                                "id": str(uuid.uuid4()),
                                "job_id": job_id,
                                "name": stem_name,
                                "output_path": saved["path"],
                                "format": job["output_format"],
                                "duration_seconds": saved["duration_seconds"],
                                "sample_rate": saved["sample_rate"],
                                "file_size_bytes": saved["file_size_bytes"],
                                "created_at": now_iso(),
                            }
                        )
                    await update_job(
                        job_id,
                        {
                            "status": "completed",
                            "progress_percent": 100,
                            "progress_stage": "complete",
                            "processing_time_seconds": result["processing_time_seconds"],
                            "completed_at": now_iso(),
                        },
                    )
                    self.emit(job_id, "complete", {"job_id": job_id})
                except Exception as exc:  # noqa: BLE001
                    await update_job(job_id, {"status": "failed", "error_message": str(exc), "completed_at": now_iso()})
                    self.emit(job_id, "error", {"message": str(exc)})


@asynccontextmanager
async def lifespan(app: FastAPI):
    config.ensure_directories()
    await init_db()
    state = AppState()
    app.state.engine = state.engine
    app.state.queue = state.queue
    app.state.events = state.events
    app.state.config = config
    app.state.get_settings = state.get_settings
    app.state.process_queue = state.process_queue
    await state.engine.load_model()
    yield


app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3457", "tauri://localhost"],
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in [health.router, separate.router, jobs.router, history.router, audio_stream.router, export.router, settings.router]:
    app.include_router(r, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=config.API_PORT, reload=True)
