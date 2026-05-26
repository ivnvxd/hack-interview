import os

from dotenv import load_dotenv

load_dotenv()

APPLICATION_WIDTH = 85
THEME = "DarkGray12"

OUTPUT_FILE_NAME = "record.wav"
SAMPLE_RATE = 48000

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

_provider = os.getenv("LLM_PROVIDER", "groq").strip().lower()
LLM_PROVIDER = _provider if _provider in {"groq", "openai"} else "groq"

PROVIDER_MODELS = {
    "groq": [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "llama3-8b-8192",
        "llama3-70b-8192",
    ],
    "openai": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
}

PROVIDER_TRANSCRIPTION_MODELS = {
    "groq": "whisper-large-v3-turbo",
    "openai": "whisper-1",
}

MODELS = PROVIDER_MODELS[LLM_PROVIDER]
DEFAULT_MODEL = MODELS[0]
TRANSCRIPTION_MODEL = PROVIDER_TRANSCRIPTION_MODELS[LLM_PROVIDER]

DEFAULT_POSITION = "Python Developer"
