from __future__ import annotations

import threading
import time

import torch
import torchaudio
from demucs.apply import apply_model
from demucs.pretrained import get_model


class DemucsEngine:
    """Wraps Demucs model for audio stem separation."""

    def __init__(self, model_name: str = "htdemucs", num_threads: int = 6):
        self.model_name = model_name
        self.num_threads = num_threads
        self.device = "cpu"
        self.model = None
        self.loaded = False
        self.processing = False
        self._lock = threading.Lock()
        self.current_job_id: str | None = None
        self.progress_callback = None

    async def load_model(self):
        torch.set_num_threads(self.num_threads)
        torch.set_float32_matmul_precision("medium")
        self.model = get_model(self.model_name)
        self.model.to(self.device)
        self.model.eval()
        self.loaded = True

    async def switch_model(self, model_name: str):
        self.model_name = model_name
        self.loaded = False
        await self.load_model()

    def get_stem_names(self) -> list[str]:
        if self.model is None:
            return ["vocals", "drums", "bass", "other"]
        return [s for s in self.model.sources]

    async def separate(self, audio_path: str, job_id: str, progress_callback=None) -> dict:
        if self.processing:
            raise RuntimeError("Separation already in progress")

        with self._lock:
            self.processing = True
            self.current_job_id = job_id
            self.progress_callback = progress_callback
            try:
                if progress_callback:
                    progress_callback({"stage": "analyzing", "percent": 5})
                wav, sr = torchaudio.load(audio_path)
                if sr != self.model.samplerate:
                    wav = torchaudio.transforms.Resample(sr, self.model.samplerate)(wav)
                    sr = self.model.samplerate
                if wav.shape[0] == 1:
                    wav = wav.repeat(2, 1)
                elif wav.shape[0] > 2:
                    wav = wav[:2]
                wav = wav.unsqueeze(0).to(self.device)

                if progress_callback:
                    progress_callback({"stage": "separating", "percent": 15})

                start = time.time()
                with torch.no_grad():
                    sources = apply_model(self.model, wav, device=self.device, progress=True, num_workers=0)
                elapsed = time.time() - start

                if progress_callback:
                    progress_callback({"stage": "encoding", "percent": 85})

                stems = {}
                for i, name in enumerate(self.get_stem_names()):
                    stems[name] = sources[0, i]

                if progress_callback:
                    progress_callback({"stage": "complete", "percent": 100})

                return {"stems": stems, "sample_rate": sr, "processing_time_seconds": elapsed}
            finally:
                self.processing = False
                self.current_job_id = None
                self.progress_callback = None
