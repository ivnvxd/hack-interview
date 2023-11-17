from typing import Any, Dict

import PySimpleGUI as sg
from loguru import logger

from src import audio, gpt_query
from src.button import OFF_IMAGE, ON_IMAGE


def recording_event(window: sg.Window) -> None:
    button: sg.Element = window["-RECORD_BUTTON-"]
    button.metadata.state = not button.metadata.state
    button.update(image_data=ON_IMAGE if button.metadata.state else OFF_IMAGE)

    # Record audio
    if button.metadata.state:
        window.perform_long_operation(lambda: audio.record(button), "-RECORDED-")


def transcribe_event(window: sg.Window) -> None:
    transcribed_text: sg.Element = window["-TRANSCRIBED_TEXT-"]
    transcribed_text.update("Transcribing audio...")

    # Transcribe audio
    window.perform_long_operation(gpt_query.transcribe_audio, "-WHISPER-")


def answer_events(window: sg.Window, values: Dict[str, Any]) -> None:
    transcribed_text: sg.Element = window["-TRANSCRIBED_TEXT-"]
    quick_answer: sg.Element = window["-QUICK_ANSWER-"]
    full_answer: sg.Element = window["-FULL_ANSWER-"]

    # Get audio transcript and update text area
    audio_transcript: str = values["-WHISPER-"]
    transcribed_text.update(audio_transcript)

    # Get model and position
    model: str = values["-MODEL_COMBO-"]
    position: str = values["-POSITION_INPUT-"]

    # Generate quick answer
    logger.debug("Generating quick answer...")
    quick_answer.update("Generating quick answer...")
    window.perform_long_operation(
        lambda: gpt_query.generate_answer(
            audio_transcript,
            short_answer=True,
            temperature=0,
            model=model,
            position=position,
        ),
        "-QUICK_ANSWER-",
    )

    # Generate full answer
    logger.debug("Generating full answer...")
    full_answer.update("Generating full answer...")
    window.perform_long_operation(
        lambda: gpt_query.generate_answer(
            audio_transcript,
            short_answer=False,
            temperature=0.7,
            model=model,
            position=position,
        ),
        "-FULL_ANSWER-",
    )
