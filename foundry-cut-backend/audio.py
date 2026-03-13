"""Audio utilities for Foundry Cut."""

from __future__ import annotations

from pathlib import Path
import shutil
import zipfile

import torch
import torchaudio
from pydub import AudioSegment

SUPPORTED_FORMATS = [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma"]


def validate_audio_file(file_path: str) -> dict:
    path = Path(file_path)
    if not path.exists():
        return {"valid": False, "error": "File not found"}
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        return {"valid": False, "error": f"Unsupported format: {path.suffix}"}
    if (path.stat().st_size / (1024 * 1024)) > 500:
        return {"valid": False, "error": "File too large"}
    try:
        info = torchaudio.info(str(path))
        duration = info.num_frames / info.sample_rate
        if duration > 30 * 60:
            return {"valid": False, "error": "Audio too long"}
        if duration < 1.0:
            return {"valid": False, "error": "Audio too short"}
        return {
            "valid": True,
            "error": None,
            "duration_seconds": duration,
            "sample_rate": info.sample_rate,
            "channels": info.num_channels,
            "format": path.suffix.lower().lstrip("."),
            "file_size_bytes": path.stat().st_size,
        }
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "error": f"Could not read audio: {exc}"}


def save_stem(waveform: torch.Tensor, sample_rate: int, output_path: str, format: str = "wav", target_sample_rate: int = 44100) -> dict:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if sample_rate != target_sample_rate:
        waveform = torchaudio.transforms.Resample(sample_rate, target_sample_rate)(waveform)
        sample_rate = target_sample_rate

    if format == "wav":
        torchaudio.save(str(path), waveform, sample_rate, encoding="PCM_S", bits_per_sample=16)
    elif format in ("mp3", "flac"):
        temp_wav = path.with_suffix(".tmp.wav")
        torchaudio.save(str(temp_wav), waveform, sample_rate, encoding="PCM_S", bits_per_sample=16)
        audio = AudioSegment.from_wav(str(temp_wav))
        audio.export(str(path), format=format, bitrate="320k" if format == "mp3" else None)
        temp_wav.unlink(missing_ok=True)
    else:
        raise ValueError(f"Unsupported output format: {format}")

    return {
        "path": str(path),
        "duration_seconds": waveform.shape[-1] / sample_rate,
        "file_size_bytes": path.stat().st_size,
        "sample_rate": sample_rate,
    }


def convert_audio(input_path: str, output_path: str, out_format: str) -> str:
    src = AudioSegment.from_file(input_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    src.export(output_path, format=out_format, bitrate="320k" if out_format == "mp3" else None)
    return output_path


def copy_audio(src: str, dst: str) -> None:
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def create_stems_zip(stem_paths: list[dict], output_path: str, original_filename: str) -> str:
    base_name = Path(original_filename).stem
    zip_path = Path(output_path) / f"{base_name}_stems.zip"
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for stem in stem_paths:
            stem_file = Path(stem["path"])
            zf.write(str(stem_file), f"{base_name}/{stem['name']}{stem_file.suffix}")
    return str(zip_path)


def get_audio_waveform_data(file_path: str, num_points: int = 200) -> list[float]:
    wav, _ = torchaudio.load(file_path)
    if wav.shape[0] > 1:
        wav = wav.mean(dim=0, keepdim=True)
    wav = wav.squeeze()
    chunk_size = max(1, len(wav) // num_points)
    points: list[float] = []
    for i in range(0, len(wav), chunk_size):
        chunk = wav[i : i + chunk_size]
        points.append(float(chunk.abs().max()))
        if len(points) >= num_points:
            break
    max_val = max(points) if points else 1.0
    return [p / max_val for p in points] if max_val > 0 else points
