from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from loguru import logger

from src.config import (
    DEFAULT_MODEL,
    DEFAULT_POSITION,
    GROQ_WHISPER_MODEL,
    LLM_PROVIDER,
    OPENAI_WHISPER_MODEL,
    OUTPUT_FILE_NAME,
)

SYS_PREFIX: str = "You are interviewing for a "
SYS_SUFFIX: str = """ position.
You will receive an audio transcription of the question. It may not be complete. You need to understand the question and write an answer to it.\n
"""

SHORT_INSTRUCTION: str = "Concisely respond, limiting your answer to 50 words."
LONG_INSTRUCTION: str = "Before answering, take a deep breath and think one step at a time. Believe the answer in no more than 150 words."

load_dotenv()

_client: Any = None


def _get_client() -> Any:
    global _client
    if _client is None:
        if LLM_PROVIDER == "groq":
            from groq import Groq

            _client = Groq()
        else:
            from openai import OpenAI

            _client = OpenAI()
    return _client


def transcribe_audio(path_to_file: str = OUTPUT_FILE_NAME) -> str:
    """
    Transcribe audio using Groq or OpenAI Whisper API.

    Args:
        path_to_file (str, optional): Path to the audio file. Defaults to OUTPUT_FILE_NAME.

    Returns:
        str: The audio transcription or an error message.
    """
    whisper_model = (
        GROQ_WHISPER_MODEL if LLM_PROVIDER == "groq" else OPENAI_WHISPER_MODEL
    )
    logger.debug(
        f"Transcribing audio ({LLM_PROVIDER}, {whisper_model}) from: {path_to_file}..."
    )

    if not Path(path_to_file).is_file():
        message = (
            "No recording found. Press R to start recording, speak your question, "
            "press R again to stop, then press A to transcribe."
        )
        logger.error(message)
        return message

    try:
        with open(path_to_file, "rb") as audio_file:
            transcript: str = _get_client().audio.transcriptions.create(
                model=whisper_model,
                file=audio_file,
                response_format="text",
            )
    except Exception as error:
        message = f"Transcription failed: {error}"
        logger.error(message)
        return message

    logger.debug("Audio transcribed.")
    print("Transcription:", transcript)

    return transcript


def generate_answer(
    transcript: str,
    short_answer: bool = True,
    temperature: float = 0.7,
    model: str = DEFAULT_MODEL,
    position: str = DEFAULT_POSITION,
) -> str:
    """
    Generate an answer using Groq or OpenAI chat completions.

    Args:
        transcript (str): The audio transcription.
        short_answer (bool, optional): Whether to generate a short answer. Defaults to True.
        temperature (float, optional): The temperature to use. Defaults to 0.7.
        model (str, optional): The model to use. Defaults to DEFAULT_MODEL.
        position (str, optional): The position to use. Defaults to DEFAULT_POSITION.

    Returns:
        str: The generated answer or an error message.
    """
    system_prompt: str = SYS_PREFIX + position + SYS_SUFFIX
    if short_answer:
        system_prompt += SHORT_INSTRUCTION
    else:
        system_prompt += LONG_INSTRUCTION

    try:
        response = _get_client().chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
        )
    except Exception as error:
        message = f"Answer generation failed: {error}"
        logger.error(message)
        return message

    return response.choices[0].message.content
