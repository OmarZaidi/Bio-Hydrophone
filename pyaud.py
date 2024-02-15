import pyaudio
import argparse
import wave
from datetime import datetime
import os


# For use of the pyaudio package on linux:
# pip install pyaudi
# sudo apt-get install portaudio19-dev

def list_audio_devices():
    p = pyaudio.PyAudio()

    # Retrieve Information About the host API at index 0

    # Returns the following dictionary:
    # 'index': The index of the audio API.
    # 'name': The name of the audio API.
    # 'defaultInputDevice': The default input device index for this audio API.
    # 'defaultOutputDevice': The default output device index for this audio API.
    # 'deviceCount': The total number of audio devices associated with this audio API.

    # Host API allows audio applications to communicate with underlying hardware
    # In the case of the Raspberry PI, ALSA is the Host API
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')

    for i in range(0, numdevices):
        # Check if device has an input channel
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            # Print information
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


def record_audio(device_index, duration=30, output_directory=".", prefix="output"):
    p = pyaudio.PyAudio()

    # Try finally block used so that stream gets closed if error occurs
    try:
        stream = p.open(format=pyaudio.paInt16,  # Set to 16-bit audio format
                        channels=1,
                        rate=44100,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=1024)

        frames = []

        print(f"Recording for {duration} seconds...")

        # The formula (sampling rate / frames per iteration) * duration is used to calculate the
        # total number of iterations needed to cover the desired duration.
        # (44100 / 1024) gives the number of iterations required to cover one second of audio data.
        for i in range(0, int(44100 / 1024 * duration)):
            # Reads 1024 frames of audio data from input audio stream
            data = stream.read(1024)
            # Appends chunk to audio data
            frames.append(data)

        print("Recording complete.")

        # Generate a file name based on the current date and time
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        file_name = f"{prefix}_{timestamp}.wav"
        file_path = os.path.join(output_directory, file_name)

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1) #set to mono audio
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(frames)) # concatenates audio data stored in frames list into single byte string

        print(f"Recording saved as: {file_path}")

    finally:

        # Close stream and remove pyaudio object
        stream.stop_stream()
        stream.close()
        p.terminate()


def play_audio(file_path):
    p = pyaudio.PyAudio()

    try:
        wf = wave.open(file_path, 'rb')

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        print("Playing audio...")

        while data:
            stream.write(data)
            data = wf.readframes(1024)

        print("Playback complete.")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    # Create an argument parser
    # To use: python pyaud.py --flag

    parser = argparse.ArgumentParser(description="List input audio devices, record audio, and play back.")
    parser.add_argument("--list-devices", action="store_true", help="List available input audio devices")
    parser.add_argument("--record", action="store_true", help="Record audio for 30 seconds")
    parser.add_argument("--device", type=int, help="Specify the input audio device index for recording [int]")
    parser.add_argument("--play", help="Path to the audio file for playback")
    parser.add_argument("--duration", type=int, help="Specify the number of seconds to record")

    # Parse command line arguments
    args = parser.parse_args()

    if args.list_devices:
        list_audio_devices()

    elif args.record:
        if args.device is not None:
            record_audio(device_index=args.device)
        else:
            print("Please specify the input audio device index using the --device option.")

    elif args.play:
        play_audio(args.play)

    else:
        print("No action specified. Use --help to list available commands")
