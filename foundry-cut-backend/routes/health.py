import platform

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
async def health(request: Request):
    app_state = request.app.state
    engine = app_state.engine
    status = "loading"
    if engine.loaded and engine.processing:
        status = "processing"
    elif engine.loaded:
        status = "ready"
    return {
        "status": status,
        "model": engine.model_name,
        "model_loaded": engine.loaded,
        "processing": engine.processing,
        "current_job_id": engine.current_job_id,
        "queue_length": len(app_state.queue),
        "device": "cpu",
        "platform": f"{platform.system().lower()}-{platform.machine().lower()}",
    }
