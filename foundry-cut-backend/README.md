# Foundry Cut Backend

Local FastAPI backend for Foundry Cut stem separation.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 3457
```

## Notes

- CPU-only Demucs inference.
- Stores data under `~/Documents/FoundryCut`.
- Requires `ffmpeg` for MP3/FLAC conversion via pydub.
- Powered by Demucs (MIT).
