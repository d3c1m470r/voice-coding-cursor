import sounddevice as sd
import numpy as np
import time

# --- Configuration from recorder.py ---
SAMPLE_RATE = 16000
CHUNK_DURATION_S = 0.5
CHUNK_SAMPLES = int(CHUNK_DURATION_S * SAMPLE_RATE)
DEVICE_INDEX = 8 # The device we're testing

def calibrate_microphone():
    """
    Helps find a suitable SILENCE_THRESHOLD by printing the RMS value of the microphone input.
    """
    print("--- Microphone Calibration ---")
    print(f"Using device index: {DEVICE_INDEX}")
    print("This script will print the audio level (RMS) of your microphone every half second.")
    print("1. Stay silent for a few seconds to measure your background noise level.")
    print("2. Speak normally to see the audio level of your voice.")
    print("\nYour 'SILENCE_THRESHOLD' in recorder.py should be a value that is:")
    print("  - HIGHER than the background noise level.")
    print("  - LOWER than your speaking voice level.")
    print("\nPress Ctrl+C to stop.")

    def callback(indata, frames, time, status):
        if status:
            print(status)
        if indata.size > 0:
            rms = np.sqrt(np.mean(indata.astype(np.float32)**2))
            # Use carriage return to print on the same line
            print(f"Current RMS: {rms:10.2f}", end='\r')

    try:
        with sd.InputStream(device=DEVICE_INDEX, samplerate=SAMPLE_RATE, channels=1, dtype='int16', blocksize=CHUNK_SAMPLES, callback=callback):
            while True:
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nCalibration finished.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    calibrate_microphone() 