import sounddevice as sd

def list_audio_devices():
    """
    Prints a list of all available audio devices, highlighting input devices.
    """
    print("--- Available Audio Devices ---")
    try:
        devices = sd.query_devices()
        print(devices)
        
        print("\n--- Input Devices ---")
        default_input_device_index = sd.default.device[0]
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                # Check if this is the default device
                is_default = " (default)" if i == default_input_device_index else ""
                print(f"Index {i}: {device['name']}{is_default}")

    except Exception as e:
        print(f"An error occurred while querying devices: {e}")
        print("This may indicate an issue with your system's audio configuration or drivers.")

if __name__ == "__main__":
    list_audio_devices() 