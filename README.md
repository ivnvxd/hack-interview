# Hack Interview

## Overview

Hack Interview application is a tool designed to assist in job interviews using the power of Generative AI. Combining voice recognition and text generation technologies, this application transcribes interview questions and generates responses in real-time, empowering users to handle interviews with confidence and ease.

## ⚠️ Disclaimer ⚠️

> This application is a proof of concept and should be used **ethically** and **responsibly**. It is not intended to deceive or mislead during interviews. The primary purpose is to demonstrate the capabilities of AI in assisting with real-time question understanding and response generation. Users should use this tool **only** for practice and learning!

## Features

- **Real-Time Audio Processing**: Records and transcribes audio seamlessly.
- **Voice Recognition**: Uses OpenAI's Whisper model for accurate voice recognition.
- **Intelligent Response Generation**: Leverages OpenAI's GPT models for generating concise and relevant answers.
- **Cross-Platform Functionality**: Designed to work on various operating systems.
- **User-Friendly Interface**: Simple, intuitive and hideous GUI for easy interaction.

## Requirements

- **Python 3.10+**: Ensure Python is installed on your system.
- **OpenAI API Key**: To use OpenAI's GPT models, you will need an API key.
- **BlackHole for MacOS**: An essential tool for recording your computer's audio output (e.g. from Zoom calls or browser tabs). Microphone Fallback: If BlackHole isn't installed or properly configured, the application can still function by recording your microphone input.

## Installation

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/ivnvxd/hack-interview.git
   cd hack-interview
   ```

2. **Install Dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

3. **BlackHole**: If using MacOS, install [BlackHole](https://github.com/ExistentialAudio/BlackHole) and set up a [Multi Output Device](https://github.com/ExistentialAudio/BlackHole/wiki/Multi-Output-Device)

4. **Environment Setup**:
   - Add your OpenAI API key to the `.env` file. If you don't have one, you can get it [here](https://platform.openai.com/api-keys).

## Usage

- **Starting the Application**: Run `python main.py` to launch the GUI.
- *(optional)* **Setup**: You can choose the OpenAI model to use for response generation and the position you are being interviewed for. The default settings are set in the `src/config.py` file.
- **Recording**: Press `R` or click the big red toggle button to start/stop audio recording. It will create a `recording.wav` file in the project directory.
- **Transcription and Response Generation**: Press `A` or click the 'Analyze' button to transcribe the recorded audio and generate answers.
- **Viewing Responses**: Responses are displayed in the GUI, offering both a quick and detailed answer.

## Contributions

Contributions are very welcome. Please submit a pull request or create an issue.

:star: Do not forget to give the project a star if you like it! :star:

## Acknowledgments

Inspired by: [hack_interview](https://github.com/slgero/hack_interview) by [slgero](https://github.com/slgero).

Special thanks to the developers and contributors of the [OpenAI](https://openai.com/).
