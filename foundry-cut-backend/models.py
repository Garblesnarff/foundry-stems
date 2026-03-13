from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


class APIError(BaseModel):
    error: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class StemFile(BaseModel):
    id: str
    name: str
    output_path: str | None = None
    format: str
    duration_seconds: float
    sample_rate: int
    file_size_bytes: int
    waveform: list[float] | None = None
    created_at: str


class Job(BaseModel):
    id: str
    status: Literal["queued", "processing", "completed", "failed", "cancelled"]
    input_filename: str
    input_path: str | None = None
    output_dir: str | None = None
    model: str
    stems: list[str]
    output_format: str
    sample_rate: int
    input_duration_seconds: float | None = None
    input_sample_rate: int | None = None
    input_channels: int | None = None
    input_format: str | None = None
    progress_percent: float = 0
    progress_stage: str | None = None
    processing_time_seconds: float | None = None
    error_message: str | None = None
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    queue_position: int | None = None
    stem_files: list[StemFile] | None = None


class JobResponse(BaseModel):
    job: Job


class BatchJobResponse(BaseModel):
    jobs: list[Job]


class SettingsResponse(BaseModel):
    model: str
    output_format: str
    sample_rate: int
    num_threads: int
    output_directory: str
    auto_cleanup_days: int


class SettingsPatchRequest(BaseModel):
    model: str | None = None
    output_format: str | None = None
    sample_rate: int | None = None
    num_threads: int | None = None
    output_directory: str | None = None
    auto_cleanup_days: int | None = None


class ExportStemRequest(BaseModel):
    job_id: str
    stems: list[str]
    format: Literal["wav", "mp3", "flac"] = "wav"
    mode: Literal["zip", "individual"] = "zip"


class ExportBatchItem(BaseModel):
    job_id: str
    stems: list[str]


class ExportBatchRequest(BaseModel):
    jobs: list[ExportBatchItem]
    format: Literal["wav", "mp3", "flac"] = "wav"
