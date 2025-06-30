# --- Audio Settings ---
SAMPLE_RATE = 16000  # Hertz (Whisper prefers 16kHz)
CHANNELS = 1  # Mono
CHUNK_DURATION_S = 0.5  # Duration of each audio chunk in seconds
CHUNK_SAMPLES = int(CHUNK_DURATION_S * SAMPLE_RATE)
DEVICE_INDEX = 7 # Use check_devices.py to find the correct index for your microphone.

# --- Silence Detection ---
SILENCE_THRESHOLD = 1000  # RMS value to determine silence. Calibrate this using calibrate.py.
SILENCE_DURATION_S = 2.0  # Seconds of silence to trigger end of recording.

# --- Hotkey ---
HOTKEY_TOGGLE = '<ctrl>+<alt>+s'

# --- Whisper Settings ---
LANGUAGE = "en"

# --- File Settings ---
OUTPUT_FILENAME = "output.wav" 