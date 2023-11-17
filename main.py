from typing import Any, Tuple

import PySimpleGUI as sg
from loguru import logger

from src import gui, handlers


def main() -> None:
    window: sg.Window = gui.initialize_window()
    logger.debug("Application started.")

    while True:
        event: str
        values: Tuple[str, Any]
        event, values = window.read()

        if event in ["-CLOSE_BUTTON-", sg.WIN_CLOSED]:
            logger.debug("Closing...")
            break

        # If the user is not focused on the position input, process the events
        focused_element: sg.Element = window.find_element_with_focus()
        if not focused_element or focused_element.Key != "-POSITION_INPUT-":
            if event in ("r", "R", "-RECORD_BUTTON-"):
                handlers.recording_event(window)
            elif event in ("a", "A", "-ANALYZE_BUTTON-"):
                handlers.transcribe_event(window)

        # If the user is focused on the position input
        if event[:6] in ("Return", "Escape"):
            window["-ANALYZE_BUTTON-"].set_focus()

        # When the transcription is ready
        elif event == "-WHISPER-":
            handlers.answer_events(window, values)

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

    window.close()


if __name__ == "__main__":
    main()
