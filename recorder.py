import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import collections
import whisper
import threading

# --- Configuration ---
SAMPLE_RATE = 16000  # Hertz (Whisper prefers 16kHz)
OUTPUT_FILENAME = "output.wav"
CHANNELS = 1  # Mono
CHUNK_DURATION_S = 0.5  # Duration of each audio chunk in seconds
CHUNK_SAMPLES = int(CHUNK_DURATION_S * SAMPLE_RATE)
SILENCE_THRESHOLD = 1000  # RMS value to determine silence. This might need adjustment based on your mics input level.
SILENCE_DURATION_S = 2.0  # Seconds of silence to trigger end of recording.
DEVICE_INDEX = 7 # Using 'pulse' directly (device 7) instead of 'default' for stability.

# --- Global State ---
recording_finished = threading.Event()
WHISPER_MODEL = None

def initialize_whisper():
    """Loads the Whisper model into a global variable."""
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        print("Loading Whisper model (small)...")
        WHISPER_MODEL = whisper.load_model("small")
        print("Whisper model loaded.")

def record_until_silence():
    """
    Records audio from the default microphone, automatically stopping after a period of silence.
    The recording only starts after the first sound is detected.
    Returns the recorded audio data as a NumPy array.
    """
    print("Starting recording. Speak into the microphone.")
    print(f"Waiting for sound... (Silence threshold: {SILENCE_THRESHOLD})")

    recorded_frames = []
    is_recording_started = False
    silence_chunks = 0
    num_silence_chunks_to_stop = int(SILENCE_DURATION_S / CHUNK_DURATION_S)

    # Use a deque to store the last few chunks to catch the start of speech
    pre_speech_buffer_size = 2 # Number of chunks before speech starts
    pre_speech_buffer = collections.deque(maxlen=pre_speech_buffer_size)
    recording_finished.clear()

    # We'll ignore the first few audio chunks to allow the microphone to stabilize.
    chunks_processed = 0
    chunks_to_ignore = 1  # Corresponds to 0.5s of audio

    def callback(indata, frames, time, status):
        nonlocal is_recording_started, silence_chunks, chunks_processed
        if status:
            print(status, flush=True)

        # Ignore initial audio chunks to prevent capturing initialization noise.
        chunks_processed += 1
        if chunks_processed <= chunks_to_ignore:
            return

        if indata.size == 0:
            return

        rms = np.sqrt(np.mean(indata.astype(np.float32)**2))
        
        pre_speech_buffer.append(indata.copy())

        if is_recording_started:
            recorded_frames.append(indata.copy())
            if rms > SILENCE_THRESHOLD:
                silence_chunks = 0
            else:
                silence_chunks += 1
                if silence_chunks >= num_silence_chunks_to_stop:
                    recording_finished.set() # Signal that recording is done
                    raise sd.CallbackStop
        elif rms > SILENCE_THRESHOLD:
            print("Sound detected, recording started...")
            is_recording_started = True
            for chunk in pre_speech_buffer:
                recorded_frames.append(chunk)
            pre_speech_buffer.clear()

    try:
        with sd.InputStream(device=DEVICE_INDEX, samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=CHUNK_SAMPLES, dtype='int16', callback=callback) as stream:
            recording_finished.wait() # Wait here until the callback signals us to stop

    except Exception as e:
        print(f"An error occurred during recording: {e}")
        return None

    print("Recording stopped.")
    if not recorded_frames:
        print("No audio was recorded.")
        return None
    
    return np.concatenate(recorded_frames, axis=0)

def transcribe_audio(audio_data):
    """
    Transcribes the given audio data using the pre-loaded Whisper model.
    """
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        # This is a fallback, but initialization should happen at startup.
        initialize_whisper()

    print("Transcribing audio...")

    # Whisper expects a 1D float32 NumPy array
    audio_1d = audio_data.flatten()
    audio_float32 = audio_1d.astype(np.float32) / 32768.0

    result = WHISPER_MODEL.transcribe(audio_float32, fp16=False, language="en")

    print("Transcription complete.")
    return result['text']

if __name__ == "__main__":
    print("Starting audio recording process...")
    audio_data = record_until_silence()
    
    if audio_data is not None and audio_data.size > 0:
        print("Audio recording finished. Got audio data.")
        # The line to save the file has been removed.

        print("Starting transcription... This may take a moment, especially on first run.")
        transcribed_text = transcribe_audio(audio_data)
        print("Transcription finished.")
        
        if transcribed_text:
            print("\n--- Transcribed Text ---")
            print(transcribed_text)
        else:
            print("\n--- Transcribed Text ---")
            print("[Whisper could not transcribe the audio or the audio was silent.]")
    else:
        print("No audio data received from recording. Exiting.") 