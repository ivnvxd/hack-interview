import sys
import threading
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import PySimpleGUI as sg
import sounddevice as sd
import soundfile as sf
from loguru import logger

from src.config import OUTPUT_FILE_NAME, SAMPLE_RATE

_PREFERRED_HOSTAPIS = ("MME", "Windows DirectSound", "Windows WASAPI")

# Devices that capture speaker / call audio (not a physical mic).
_SYSTEM_DEVICE_KEYWORDS = (
    "blackhole",
    "stereo mix",
    "stereomix",
    "what u hear",
    "wave out",
    "loopback",
    "cable output",
    "vb-audio",
    "vb audio",
    "virtual cable",
    "soundflower",
)


def _hostapi_name(device: Dict[str, Any]) -> str:
    return sd.query_hostapis()[device["hostapi"]]["name"]


def _is_system_device(name: str) -> bool:
    lower = name.lower()
    return any(keyword in lower for keyword in _SYSTEM_DEVICE_KEYWORDS)


def _device_priority(device_id: int) -> int:
    """Lower is better. Prefer stable host APIs on Windows."""
    api = _hostapi_name(sd.query_devices(device_id))
    if sys.platform == "win32":
        order = {name: i for i, name in enumerate(_PREFERRED_HOSTAPIS)}
        return order.get(api, len(_PREFERRED_HOSTAPIS))
    return 0


def find_system_device_id() -> Optional[int]:
    """
    Find a device that records system/call audio (Teams, Zoom, browser).

    Windows: enable Stereo Mix, or install VB-Audio Cable (see README).
    macOS: install BlackHole and route call audio to it.
    """
    candidates: List[Tuple[int, int]] = []
    for device_id, device in enumerate(sd.query_devices()):
        if device["max_input_channels"] < 1:
            continue
        if _is_system_device(device["name"]):
            candidates.append((device_id, _device_priority(device_id)))

    if not candidates:
        return None

    device_id = min(candidates, key=lambda item: item[1])[0]
    device = sd.query_devices(device_id)
    logger.debug(
        f"Using system audio device: {device['name']} ({_hostapi_name(device)})"
    )
    return device_id


def find_microphone_device_id() -> Optional[int]:
    """Find a normal microphone, excluding virtual system-capture devices."""
    system_id = find_system_device_id()
    candidates: List[Tuple[int, int]] = []

    for device_id, device in enumerate(sd.query_devices()):
        if device["max_input_channels"] < 1:
            continue
        if device_id == system_id:
            continue
        if _is_system_device(device["name"]):
            continue
        candidates.append((device_id, _device_priority(device_id)))

    if candidates:
        device_id = min(candidates, key=lambda item: item[1])[0]
        device = sd.query_devices(device_id)
        logger.debug(
            f"Using microphone: {device['name']} ({_hostapi_name(device)})"
        )
        return device_id

    default_input = sd.default.device[0]
    if default_input is not None and default_input >= 0:
        device = sd.query_devices(default_input)
        if not _is_system_device(device["name"]):
            logger.debug(f"Using default input device: {device['name']}")
            return default_input

    return None


def resolve_device_ids(audio_source: str) -> List[int]:
    """Return device id(s) to record for the given source mode."""
    source = audio_source.lower()
    mic_id = find_microphone_device_id()
    system_id = find_system_device_id()

    if source == "mic":
        return [mic_id] if mic_id is not None else []
    if source == "system":
        return [system_id] if system_id is not None else []
    if source == "both":
        ids = []
        if system_id is not None:
            ids.append(system_id)
        if mic_id is not None and mic_id not in ids:
            ids.append(mic_id)
        return ids

    logger.warning(f"Unknown audio source '{audio_source}', using microphone.")
    return [mic_id] if mic_id is not None else []


def _device_sample_rate(device_id: int) -> int:
    info = sd.query_devices(device_id, "input")
    rate = int(info["default_samplerate"])
    return rate if rate > 0 else SAMPLE_RATE


def _to_mono(audio_data: np.ndarray) -> np.ndarray:
    if audio_data.ndim == 1:
        return audio_data
    return audio_data.mean(axis=1)


def _mix_tracks(tracks: List[np.ndarray]) -> np.ndarray:
    if len(tracks) == 1:
        return tracks[0]
    min_len = min(track.shape[0] for track in tracks)
    mono_tracks = [_to_mono(track[:min_len]) for track in tracks]
    mixed = np.sum(mono_tracks, axis=0)
    peak = np.max(np.abs(mixed))
    if peak > 1.0:
        mixed = mixed / peak
    return mixed


def _record_device(
    device_id: int,
    button: sg.Element,
    frames: List[np.ndarray],
    lock: threading.Lock,
) -> None:
    samplerate = _device_sample_rate(device_id)
    device_info = sd.query_devices(device_id, "input")
    channels = min(int(device_info["max_input_channels"]), 2)

    def callback(
        indata: np.ndarray,
        frame_count: int,
        time_info: Any,
        status: sd.CallbackFlags,
    ) -> None:
        if status:
            logger.warning(f"Audio stream status: {status}")
        if button.metadata.state:
            with lock:
                frames.append(indata.copy())

    with sd.InputStream(
        samplerate=samplerate,
        device=device_id,
        channels=channels,
        dtype="float32",
        callback=callback,
        blocksize=int(samplerate * 0.1),
    ):
        while button.metadata.state:
            sd.sleep(100)


def record(button: sg.Element, audio_source: str = "system") -> None:
    """
    Record audio while the record button is active.

    Args:
        button: The record toggle button.
        audio_source: "mic", "system", or "both".
    """
    logger.debug(f"Recording (source={audio_source})...")
    device_ids = resolve_device_ids(audio_source)

    if not device_ids:
        if audio_source.lower() in ("system", "both"):
            logger.error(
                "No system audio device found. Enable Stereo Mix in Windows Sound "
                "settings, or install VB-Audio Virtual Cable (see README)."
            )
        else:
            logger.error("No microphone found.")
        return

    if audio_source.lower() in ("system", "both") and find_system_device_id() is None:
        logger.warning(
            "System audio device not found; only microphone will be used. "
            "See README to capture Teams/Zoom audio."
        )

    all_frames: List[List[np.ndarray]] = [[] for _ in device_ids]
    locks = [threading.Lock() for _ in device_ids]
    errors: List[str] = []

    def worker(index: int, device_id: int) -> None:
        try:
            _record_device(device_id, button, all_frames[index], locks[index])
        except Exception as e:
            errors.append(str(e))
            logger.error(f"Recording error on device {device_id}: {e}")

    threads = [
        threading.Thread(target=worker, args=(i, device_id), daemon=True)
        for i, device_id in enumerate(device_ids)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    if errors and not any(all_frames):
        return

    tracks = []
    for frames in all_frames:
        if frames:
            tracks.append(np.concatenate(frames, axis=0))

    if not tracks:
        logger.warning("No audio recorded.")
        return

    audio_data = _mix_tracks(tracks)
    samplerate = _device_sample_rate(device_ids[0])
    save_audio_file(audio_data, samplerate=samplerate)


def save_audio_file(
    audio_data: np.ndarray,
    output_file_name: str = OUTPUT_FILE_NAME,
    samplerate: int = SAMPLE_RATE,
) -> None:
    """Save audio data to a WAV file."""
    if audio_data.ndim == 1:
        data = audio_data
    else:
        data = audio_data

    sf.write(
        file=output_file_name,
        data=data,
        samplerate=samplerate,
        format="WAV",
        subtype="PCM_16",
    )
    logger.debug(f"Audio saved to: {output_file_name}...")
