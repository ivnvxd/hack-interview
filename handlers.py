from pathlib import Path
from typing import Any, Dict

import PySimpleGUI as sg
from loguru import logger

from src import audio, gpt_query
from src.button import OFF_IMAGE, ON_IMAGE
from src.config import AUDIO_SOURCE_OPTIONS, OUTPUT_FILE_NAME


def handle_events(window: sg.Window, event: str, values: Dict[str, Any]) -> None:
    """
    Handle the events. Record audio, transcribe audio, generate quick and full answers.

    Args:
        window (sg.Window): The window element.
        event (str): The event.
        values (Dict[str, Any]): The values of the window.
    """
    # If the user is not focused on the position input, process the events
    focused_element: sg.Element = window.find_element_with_focus()
    if not focused_element or focused_element.Key != "-POSITION_INPUT-":
        if event in ("r", "R", "-RECORD_BUTTON-"):
            recording_event(window)
        elif event in ("a", "A", "-ANALYZE_BUTTON-"):
            transcribe_event(window)

    # If the user is focused on the position input
    if event[:6] in ("Return", "Escape"):
        window["-ANALYZE_BUTTON-"].set_focus()

    elif event == "-RECORDED-":
        _recording_finished(window)

    # When the transcription is ready
    elif event == "-WHISPER-":
        answer_events(window, values)

    # When the quick answer is ready
    elif event == "-QUICK_ANSWER-":
        logger.debug("Quick answer generated.")
        print("Quick answer:", values["-QUICK_ANSWER-"])
        window["-QUICK_ANSWER-"].update(values["-QUICK_ANSWER-"])

    # When the full answer is ready
    elif event == "-FULL_ANSWER-":
        logger.debug("Full answer generated.")
        print("Full answer:", values["-FULL_ANSWER-"])
        window["-FULL_ANSWER-"].update(values["-FULL_ANSWER-"])


def _recording_finished(window: sg.Window) -> None:
    """Notify user if recording failed (common when system audio is not configured)."""
    if Path(OUTPUT_FILE_NAME).is_file():
        return

    label = window["-AUDIO_SOURCE_COMBO-"].get()
    source = AUDIO_SOURCE_OPTIONS.get(label, "system")
    transcribed_text: sg.Element = window["-TRANSCRIBED_TEXT-"]

    if source in ("system", "both"):
        transcribed_text.update(
            "No system audio captured. Enable Stereo Mix in Windows Sound settings, "
            "or install VB-Audio Virtual Cable (see README). Then set Audio to "
            "System (Teams/Zoom) and try again."
        )
    else:
        transcribed_text.update(
            "No audio recorded. Check your microphone and try again."
        )


def recording_event(window: sg.Window) -> None:
    """
    Handle the recording event. Record audio and update the record button.

    Args:
        window (sg.Window): The window element.
    """
    button: sg.Element = window["-RECORD_BUTTON-"]
    button.metadata.state = not button.metadata.state
    button.update(image_data=ON_IMAGE if button.metadata.state else OFF_IMAGE)

    # Record audio
    if button.metadata.state:
        label = window["-AUDIO_SOURCE_COMBO-"].get()
        source = AUDIO_SOURCE_OPTIONS.get(label, "system")
        window.perform_long_operation(
            lambda: audio.record(button, source), "-RECORDED-"
        )


def transcribe_event(window: sg.Window) -> None:
    """
    Handle the transcribe event. Transcribe audio and update the text area.

    Args:
        window (sg.Window): The window element.
    """
    transcribed_text: sg.Element = window["-TRANSCRIBED_TEXT-"]
    record_button: sg.Element = window["-RECORD_BUTTON-"]

    if record_button.metadata.state:
        transcribed_text.update(
            "Still recording. Press R again to stop recording, then press A."
        )
        return

    if not Path(OUTPUT_FILE_NAME).is_file():
        transcribed_text.update(
            "No recording found. Press R to record, R again to stop, then press A."
        )
        return

    transcribed_text.update("Transcribing audio...")
    window.perform_long_operation(gpt_query.transcribe_audio, "-WHISPER-")


def answer_events(window: sg.Window, values: Dict[str, Any]) -> None:
    """
    Handle the answer events. Generate quick and full answers and update the text areas.

    Args:
        window (sg.Window): The window element.
        values (Dict[str, Any]): The values of the window.
    """
    transcribed_text: sg.Element = window["-TRANSCRIBED_TEXT-"]
    quick_answer: sg.Element = window["-QUICK_ANSWER-"]
    full_answer: sg.Element = window["-FULL_ANSWER-"]

    # Get audio transcript and update text area
    audio_transcript: str = values["-WHISPER-"]
    transcribed_text.update(audio_transcript)

    if audio_transcript.startswith(("No recording found", "Transcription failed")):
        return

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
