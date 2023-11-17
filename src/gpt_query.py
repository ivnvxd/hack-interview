from dotenv import load_dotenv
from loguru import logger
from openai import ChatCompletion, OpenAI

from src.config import DEFAULT_MODEL, DEFAULT_POSITION, OUTPUT_FILE_NAME

SYS_PREFIX: str = "You are interviewing for a "
SYS_SUFFIX: str = """ position.
You will receive an audio transcription of the question. It may not be complete. You need to understand the question and write an answer to it.\n
"""

SHORT_INSTRUCTION: str = "Concisely respond, limiting your answer to 50 words."
LONG_INSTRUCTION: str = "Before answering, take a deep breath and think one step at a time. Believe the answer in no more than 150 words."

load_dotenv()

client: OpenAI = OpenAI()


def transcribe_audio(path_to_file: str = OUTPUT_FILE_NAME) -> str:
    """
    Transcribe audio from a file using the OpenAI Whisper API.

    Args:
        path_to_file (str, optional): Path to the audio file. Defaults to OUTPUT_FILE_NAME.

    Returns:
        str: The audio transcription.
    """
    logger.debug(f"Transcribing audio from: {path_to_file}...")

    with open(path_to_file, "rb") as audio_file:
        try:
            transcript: str = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="text"
            )
        except Exception as error:
            logger.error(f"Can't transcribe audio: {error}")
            raise error

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
    Generate an answer to the question using the OpenAI API.

    Args:
        transcript (str): The audio transcription.
        short_answer (bool, optional): Whether to generate a short answer. Defaults to True.
        temperature (float, optional): The temperature to use. Defaults to 0.7.
        model (str, optional): The model to use. Defaults to DEFAULT_MODEL.
        position (str, optional): The position to use. Defaults to DEFAULT_POSITION.

    Returns:
        str: The generated answer.
    """
    # Generate system prompt
    system_prompt: str = SYS_PREFIX + position + SYS_SUFFIX
    if short_answer:
        system_prompt += SHORT_INSTRUCTION
    else:
        system_prompt += LONG_INSTRUCTION

    # Generate answer
    try:
        response: ChatCompletion = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript},
            ],
        )
    except Exception as error:
        logger.error(f"Can't generate answer: {error}")
        raise error

    return response.choices[0].message.content
