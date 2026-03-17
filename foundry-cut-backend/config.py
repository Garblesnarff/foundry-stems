import os
from pathlib import Path

APP_NAME = "Foundry Cut"
APP_VERSION = "1.0.0"
API_PORT = 3457
BASE_DIR = Path.home() / "Documents" / "FoundryCut"
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "foundry_cut.db"
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
TEMP_DIR = BASE_DIR / "temp"

DEFAULT_MODEL = "htdemucs"
SUPPORTED_MODELS = ["htdemucs", "htdemucs_ft", "htdemucs_6s", "mdx_extra"]
STEM_NAMES = ["vocals", "drums", "bass", "other"]
STEM_NAMES_6S = ["vocals", "drums", "bass", "guitar", "piano", "other"]
SUPPORTED_INPUT_FORMATS = [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma"]
SUPPORTED_OUTPUT_FORMATS = ["wav", "mp3", "flac"]
DEFAULT_OUTPUT_FORMAT = "wav"
DEFAULT_SAMPLE_RATE = 44100
MAX_FILE_SIZE_MB = 500
MAX_DURATION_MINUTES = 30

DEFAULT_NUM_THREADS = max(1, (os.cpu_count() or 4) - 2)
DEVICE = "cpu"


def ensure_directories() -> None:
    for directory in [BASE_DIR, DB_DIR, INPUT_DIR, OUTPUT_DIR, TEMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
