from __future__ import annotations

import asyncio

from fastapi import APIRouter, HTTPException, Request

from config import SUPPORTED_MODELS, SUPPORTED_OUTPUT_FORMATS
from database import fetch_settings, update_settings
from models import SettingsPatchRequest

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
async def get_settings():
    return await fetch_settings()


@router.patch("", status_code=202)
async def patch_settings(request: Request, payload: SettingsPatchRequest):
    updates = payload.model_dump(exclude_none=True)
    if "model" in updates and updates["model"] not in SUPPORTED_MODELS:
        raise HTTPException(status_code=400, detail={"error": "invalid_setting", "message": "Invalid model", "details": {}})
    if "output_format" in updates and updates["output_format"] not in SUPPORTED_OUTPUT_FORMATS:
        raise HTTPException(status_code=400, detail={"error": "invalid_setting", "message": "Invalid output format", "details": {}})

    await update_settings(updates)

    if "model" in updates:
        async def _reload():
            await request.app.state.engine.switch_model(updates["model"])

        asyncio.create_task(_reload())

    return {"accepted": True, "settings": await fetch_settings()}
