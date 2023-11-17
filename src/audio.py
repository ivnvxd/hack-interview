from typing import Any, Dict, List, Optional

import numpy as np
import sounddevice as sd
import soundfile as sf
from loguru import logger

from src.config import OUTPUT_FILE_NAME, SAMPLE_RATE


def find_blackhole_device_id() -> Optional[int]:
    devices: List[Dict[str, Any]] = sd.query_devices()
    for device_id, device in enumerate(devices):
        if "BlackHole" in device["name"]:
            return device_id

    return None


def record(button: Any) -> None:
    logger.debug("Recording...")
    frames: List[np.ndarray] = []

    # Find BlackHole device ID
    device_id: Optional[int] = find_blackhole_device_id()

    # Record audio
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, device=device_id) as stream:
            while button.metadata.state:
                data: np.ndarray
                overflowed: bool
                data, overflowed = stream.read(SAMPLE_RATE)
                if overflowed:
                    logger.warning("Audio buffer overflowed")
                frames.append(data)

    except Exception as e:
        logger.error(f"An error occurred during recording: {e}")

    # Save audio file
    if frames:
        audio_data: np.ndarray = np.vstack(frames)
        save_audio_file(audio_data)
    else:
        logger.warning("No audio recorded.")


def save_audio_file(
    audio_data: np.ndarray, output_file_name: str = OUTPUT_FILE_NAME
) -> None:
    sf.write(
        file=output_file_name,
        data=audio_data,
        samplerate=SAMPLE_RATE,
        format="WAV",
        subtype="PCM_16",
    )
    logger.debug(f"Audio saved to: {output_file_name}...")
