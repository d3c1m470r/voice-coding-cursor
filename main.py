from pynput import keyboard
from recorder import record_until_silence, transcribe_audio, initialize_whisper
import threading

# --- Configuration ---
# Note: Using GlobalHotKeys is often more reliable for system-wide hotkeys.
HOTKEY_TOGGLE = '<ctrl>+<alt>+s'

# --- Global State ---
voice_mode_thread = None
voice_mode_active = threading.Event()

def voice_mode_loop():
    """The main loop for continuous voice coding."""
    while voice_mode_active.is_set():
        print("\nListening for speech...")
        audio_data = record_until_silence()
        
        # Check if the mode was deactivated while we were recording.
        if not voice_mode_active.is_set():
            break

        if audio_data is not None and audio_data.size > 0:
            print("Audio recorded, starting transcription...")
            transcribed_text = transcribe_audio(audio_data)
            
            if transcribed_text:
                type_text(transcribed_text)
            else:
                print("Transcription returned empty.")
        else:
            # This can happen if the stop event is triggered during recording.
            print("No audio recorded.")

def toggle_voice_mode():
    """Starts or stops the voice mode thread."""
    global voice_mode_thread
    if voice_mode_active.is_set():
        print("Deactivating voice mode...")
        voice_mode_active.clear()
        if voice_mode_thread:
            voice_mode_thread.join() # Wait for the loop to finish gracefully
        print("Voice mode deactivated.")
    else:
        print("Activating voice mode...")
        voice_mode_active.set()
        voice_mode_thread = threading.Thread(target=voice_mode_loop)
        voice_mode_thread.start()

def type_text(text):
    """Types the given text using the keyboard controller."""
    controller = keyboard.Controller()
    controller.type(text.strip())
    controller.press(keyboard.Key.enter)
    controller.release(keyboard.Key.enter)

def main():
    """Initializes the application and starts the hotkey listener."""
    print("--- Voice Coder is running ---")
    
    # Load the Whisper model at startup for a faster response time.
    initialize_whisper()
    
    print(f"Press {HOTKEY_TOGGLE} to toggle voice mode.")
    print("Press Ctrl+C in this terminal to exit.")
    
    # Use a global hotkey listener for a more robust toggle mechanism.
    with keyboard.GlobalHotKeys({
            HOTKEY_TOGGLE: toggle_voice_mode,
    }) as h:
        h.join()

if __name__ == "__main__":
    main() 