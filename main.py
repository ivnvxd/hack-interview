from typing import Any, Dict

import PySimpleGUI as sg
from loguru import logger

from src.gui import initialize_window
from src.handlers import handle_events


def main() -> None:
    """
    Main function. Initialize the window and handle the events.
    """
    window: sg.Window = initialize_window()
    logger.debug("Application started.")

    while True:
        event: str
        values: Dict[str, Any]
        event, values = window.read()

        if event in ["-CLOSE_BUTTON-", sg.WIN_CLOSED]:
            logger.debug("Closing...")
            break

        handle_events(window, event, values)

    window.close()


if __name__ == "__main__":
    main()
