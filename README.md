# Hack Interview

## Overview

Hack Interview application is a tool designed to assist in job interviews using the power of Generative AI. Combining voice recognition and text generation technologies, this application transcribes interview questions and generates responses in real-time, empowering users to handle interviews with confidence and ease.

## ⚠️ Disclaimer ⚠️

> This application is a proof of concept and should be used **ethically** and **responsibly**. It is not intended to deceive or mislead during interviews. The primary purpose is to demonstrate the capabilities of AI in assisting with real-time question understanding and response generation. Users should use this tool **only** for practice and learning!

## Features

- **Real-Time Audio Processing**: Records and transcribes audio seamlessly.
- **Voice Recognition**: Uses Groq Whisper (or OpenAI Whisper) for accurate voice recognition.
- **Intelligent Response Generation**: Uses Groq Llama models (or OpenAI GPT) for concise and relevant answers.
- **Cross-Platform Functionality**: Designed to work on various operating systems.
- **User-Friendly Interface**: Simple, intuitive and hideous GUI for easy interaction.

## Requirements

- **Python 3.10+**: Ensure Python is installed on your system.
- **Groq API Key** (recommended): Free tier at [console.groq.com](https://console.groq.com/keys). Used for Whisper transcription and Llama answers by default.
- **OpenAI API Key** (optional): Only if you set `LLM_PROVIDER=openai` in `.env`.
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
   - Copy `.env.example` to `.env`.
   - Add your Groq API key (`GROQ_API_KEY`) from [console.groq.com](https://console.groq.com/keys).
   - Default provider is Groq (`LLM_PROVIDER=groq`). For OpenAI instead, set `LLM_PROVIDER=openai` and add `OPENAI_API_KEY`.

## Usage

- **Starting the Application**: Run `python main.py` to launch the GUI.
- **Audio source**: In the GUI, set **Audio** to **System (Teams/Zoom)** for live calls (default). Use **Microphone** only when testing alone.
- **Recording**: Press `R` to start, speak or let the interviewer ask a question, press `R` again to stop. Saves `record.wav` in the project folder.
- **Transcription**: Press `A` to transcribe and generate short/full answers.

## Capture Microsoft Teams / Zoom audio (Windows)

Your **microphone only hears you**, not the interviewer. Teams plays their voice through **speakers/headphones** (system audio). Use one of these setups:

### Option A — Stereo Mix (free, if your PC supports it)

1. Right-click the **speaker icon** → **Sound settings** → **More sound settings**.
2. Open the **Recording** tab → right-click empty area → check **Show disabled devices**.
3. Enable **Stereo Mix** → Set as **Default Device** (or note its name).
4. In the app, set **Audio** to **System (Teams/Zoom)**.
5. In Teams, use your normal **speakers or headset** for call audio.

### Option B — VB-Audio Virtual Cable (works on most PCs)

1. Install [VB-Audio Virtual Cable](https://vb-audio.com/Cable/) (free).
2. In **Teams** → Settings → **Devices** → set **Speaker** to **CABLE Input**.
3. In **Windows Sound** → **Recording**, enable **CABLE Output** as default (or the app will detect it automatically).
4. Listen on your headset via Teams **Test call** or use **Listen to this device** on CABLE Output if you need to hear the call.

### During the interview

1. Set **Audio** → **System (Teams/Zoom)**.
2. When the interviewer asks a question, press **R** (record) → wait for the question → press **R** (stop).
3. Press **A** to transcribe and get answers.

Use **Both** if you want system audio plus your mic in one recording.

### macOS

Install [BlackHole](https://github.com/ExistentialAudio/BlackHole), create a **Multi-Output Device** that includes BlackHole + your headphones, and set Teams output to that device. Set **Audio** to **System (Teams/Zoom)**.

## Contributions

Contributions are very welcome. Please submit a pull request or create an issue.

## Support

Thank you for using this project! If you find it helpful and would like to support my work, kindly consider buying me a coffee. Your support is greatly appreciated!

<a href="https://www.buymeacoffee.com/ivnvxd" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

And do not forget to give the project a star if you like it! :star:

## Acknowledgments

Inspired by: [hack_interview](https://github.com/slgero/hack_interview) by [slgero](https://github.com/slgero).

Special thanks to the developers and contributors of the [OpenAI](https://openai.com/).
