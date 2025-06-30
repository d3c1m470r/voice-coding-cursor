# Voice Coding for Cursor

This project is a Python-based, hands-free coding assistant that uses the Whisper speech-to-text engine to transcribe your voice into text in near real-time. Activate it with the hotkeys, speak, and watch it get typed out in any application.

## Features

- **Voice-to-Text:** Converts spoken words into text using OpenAI's Whisper model.
- **Silence Detection:** Automatically starts recording on sound and stops after a period of silence.
- **Hotkey Activation:** Toggle the voice mode on and off with a customizable system-wide hotkey (`<ctrl>+<alt>+s`).
- **Pre-loaded Model:** The Whisper model is loaded at startup to ensure a fast and seamless transcription experience.
- **Customizable:** Easily configurable silence threshold and microphone device index to suit your environment.

## Language Support

This application defaults to English but can be configured to transcribe any of the 99 languages supported by the Whisper model. This includes languages like Spanish, French, German, Japanese, Chinese, Russian, and many more.

To change the language, you need to edit one line in `config.py`:

1.  Open the `config.py` file.
2.  Find the `LANGUAGE` variable.
3.  Change the `LANGUAGE` variable to the language you want. For example, for German, you would change it to `"de"`.

```python
# In config.py:
LANGUAGE = "de" # Changed "en" to "de"
```

For a full list of supported languages and their two-letter codes, please refer to the [official Whisper documentation](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py).

## File Overview

- **`main.py`**: The main entry point of the application. It handles hotkey listening and orchestrates the recording and transcription process.
- **`recorder.py`**: Contains all the logic for audio recording, silence detection, and interfacing with the Whisper model for transcription.
- **`config.py`**: The central configuration file. All settings, such as microphone device index, silence threshold, language, and hotkeys, are managed here.
- **`check_devices.py`**: A utility script to list all available audio devices on your system, helping you find the correct index for your microphone.
- **`calibrate.py`**: A helper script to calibrate the `SILENCE_THRESHOLD`. It prints the real-time audio level of your microphone, allowing you to find the perfect value to distinguish between ambient noise and speech.
- **`requirements.txt`**: A list of all the necessary Python packages for this project.

## Setup and Usage

Follow these steps to get the voice coding assistant up and running on your system.

### 1. Clone the Repository

```bash
git clone https://github.com/d3c1m470r/voice-coding-cursor.git
cd voice-coding-cursor
```

### 2. Create a Virtual Environment and install dependencies

It's highly recommended to use a virtual environment to manage the project's dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Your Application

You'll need to tell the application which microphone to use, how sensitive it should be, and what hotkey to use. All settings are in the `config.py` file.

1.  **Find Your Device Index:** Run the `check_devices.py` script to see a list of your audio devices.

    ```bash
    python3 check_devices.py
    ```

    Find your microphone in the list and note its `index` number.

2.  **Set the Device Index:** Open `config.py` and change the `DEVICE_INDEX` variable to the index you just found.

3.  **Calibrate the Silence Threshold:** Run the `calibrate.py` script.

    ```bash
    python3 calibrate.py
    ```

    Stay silent for a moment to see the audio level of your background noise, then speak normally. Choose a value for `SILENCE_THRESHOLD` that is higher than your background noise but lower than your speaking volume. Update the `SILENCE_THRESHOLD` variable in `config.py`.

4.  **(Optional) Configure the Hotkey:** Open `config.py` and change the `HOTKEY_TOGGLE` variable. The key combination must be a string in a format that the `pynput` library understands. For example, you can use `'<ctrl>+<alt>+h'` or `'<cmd>+<shift>+r'`.

### 4. Run the Application

Once configured, you can start the main application.

```bash
python3 main.py
```

The application will load the Whisper model and then wait for you to press the hotkey.

### 5. Start Coding with Your Voice!

- **Press `<ctrl>+<alt>+s`** to activate the voice mode.
- The application will start listening. Once it detects you speaking, it will record.

**_WARNING_** it will type anything you say where you currently stand with your cursor, then press enter, so you can prompt the models directly by simply speaking.

- When you stop speaking, it will automatically transcribe the audio and type it out.
- The default value is 2 seconds of silence, so if you stay quiet, the text gets typed out with an enter at the end.
- **Press `<ctrl>+<alt>+s`** again to deactivate the voice mode.
