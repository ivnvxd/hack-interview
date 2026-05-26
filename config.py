import os
from pathlib import Path

APPLICATION_WIDTH = 85
THEME = "DarkGray12"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE_NAME = str(PROJECT_ROOT / "record.wav")
SAMPLE_RATE = 48000

# "groq" or "openai" — set LLM_PROVIDER in .env
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

MODELS = GROQ_MODELS if LLM_PROVIDER == "groq" else OPENAI_MODELS
DEFAULT_MODEL = MODELS[0]

OPENAI_WHISPER_MODEL = "whisper-1"
GROQ_WHISPER_MODEL = "whisper-large-v3-turbo"

DEFAULT_POSITION = "Python Developer"

# Audio: mic | system | both — system captures Teams/Zoom from speakers
AUDIO_SOURCE_OPTIONS = {
    "Microphone": "mic",
    "System (Teams/Zoom)": "system",
    "Both": "both",
}
_env_source = os.getenv("AUDIO_SOURCE", "system").lower()
DEFAULT_AUDIO_SOURCE = (
    _env_source
    if _env_source in ("mic", "system", "both")
    else "system"
)
DEFAULT_AUDIO_SOURCE_LABEL = next(
    (label for label, key in AUDIO_SOURCE_OPTIONS.items() if key == DEFAULT_AUDIO_SOURCE),
    "System (Teams/Zoom)",
)
