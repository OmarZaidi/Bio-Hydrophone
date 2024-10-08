#!/usr/bin/python3.9
import sys
import pyaudio
import argparse
import wave
from datetime import datetime, timedelta
import time
import os
import json


# For use of the pyaudio package on linux:
# pip install pyaudio
# sudo apt-get install portaudio19-dev

# Class Tee allows output to write to output log and command line at the same time
class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()  # Ensure immediate flushing

    def flush(self):
        for f in self.files:
            f.flush()

def list_audio_devices(index=None, return_name=False):
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
    input_devices = 0

    # Returns name of specified device. Used in user_config.py under verify_config function
    if return_name and index is not None:
        return p.get_device_info_by_host_api_device_index(0, index-1).get('name')

    for i in range(0, numdevices):
        # Check if device has an input channel
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            input_devices += 1

            # Print information
            print("Input Device id [" + str(i + 1) + "] - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    return input_devices


# Main Function for handling recording session
def record_audio(device_index=1, duration=10, start_time=None, end_time=None, period=None,
                 sample_rate=96000, location="default", current_directory=".", prefix="output"):
    p = pyaudio.PyAudio()

    # Converts start_time string to date_time object
    if start_time is not None:
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")

        # Calculate number of recording sessions
        if end_time is not None:

            # Convert end_time into datetime and time strings into objects
            end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            period = datetime.strptime(period, "%H:%M:%S").time()

            # Make sure end_time is after start_time
            from user_config import end_time_after
            if not end_time_after(end_time, start_time):
                print("Error! end_time must be after start_time. Please check config.json parameters. Terminating program.")
                sys.exit(1)

            # Convert to timedelta object so that total_seconds can be extracted
            period = timedelta(hours=period.hour, minutes=period.minute, seconds=period.second)

            # Calculate the difference in seconds between start time and end time
            total_seconds = (end_datetime - start_datetime).total_seconds()

            # Calculate number of sessions using period
            period_seconds = period.total_seconds()
            num_sessions = round((total_seconds / period_seconds))

            # Handles case in which the number of sessions round to 0 when period_seconds is > total_seconds
            if num_sessions == 0:
                num_sessions = 1

        # If current time past start time, current time becomes new start time
        current_time = datetime.now()
        if current_time > start_datetime:
            start_datetime = current_time

    else:
        start_datetime = datetime.now()
        num_sessions = 1

    # Create output directory
    current_directory = os.getcwd()
    start_time = start_datetime.strftime("%Y%m%d_%H%M%S")
    output_directory = current_directory + "/" + location + "_" + start_time
    path = os.path.join(current_directory, output_directory)
    os.mkdir(path)

    # Open the log file
    log_file_name = f"{location}_log.txt"
    log_file_path = os.path.join(output_directory, log_file_name)
    log_file = open(log_file_path, "w")

    # Create a Tee object with sys.stdout and the log file
    tee = Tee(sys.stdout, log_file)

    # Replace sys.stdout with the Tee object
    sys.stdout = tee

    print(f"Recording for {num_sessions} session(s) with a duration of {duration} seconds")

    for index in range(1, num_sessions + 1):

        print("\n")

        # Delay recording until start time is reached
        if start_time is not None:
            current_time = datetime.now().time()
            print(f'Current date and time: {current_time}')

            # Calculate the difference in seconds
            delay_seconds = (start_datetime - datetime.now()).total_seconds()

            # If start time has passed already, there is no delay
            if delay_seconds > 0:
                print(f"Waiting for {delay_seconds} seconds until the start time ({start_datetime}) is reached.")
                for _ in range(round(delay_seconds)):
                    time.sleep(1)
                # time.sleep(delay_seconds)
            else:
                # If current datetime is past start_datetime, current datetime becomes new start_datetime
                # Still conducts all recording sessions
                start_datetime = datetime.now()

        # Try-finally block used so that stream gets closed if error occurs
        try:
            stream = p.open(format=pyaudio.paInt16,  # Set to 16-bit audio format
                            channels=1,
                            rate=sample_rate,
                            input=True,
                            input_device_index=device_index,
                            frames_per_buffer=1024)

            frames = []

            print(f"Recording audio with sample rate {sample_rate}, duration {duration}s")

            # The formula (sampling rate / frames per iteration) * duration is used to calculate the
            # total number of iterations needed to cover the desired duration.
            # (44100 / 1024) gives the number of iterations required to cover one second of audio data.
            for i in range(0, int((sample_rate / 1024) * duration)):
                # Reads 1024 frames of audio data from input audio stream
                data = stream.read(1024)
                # Appends chunk to audio data
                frames.append(data)

            print("Recording complete.")
            current_datetime = datetime.now()
            current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            print("Current date and time:", current_datetime_str)

            # Generate a file name based on the index and save to output directory
            file_name = f"{prefix}_{index}.wav"
            file_path = os.path.join(output_directory, file_name)

            with wave.open(file_path, 'wb') as wf:
                wf.setnchannels(1)  # set to mono audio
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
                wf.setframerate(sample_rate)
                wf.writeframes(b''.join(frames))  # concatenates audio data stored in frames list into single byte string
                wf.close()

            print(f"Recording saved as: {file_path}")

            # Calculate next recording session start time if there is more than one session
            if num_sessions > 1:
                start_datetime = start_datetime + timedelta(seconds=period_seconds)

        except KeyboardInterrupt:
            print("Recording stopped by keyboard interrupt")
            pass

        finally:
            # Close stream and remove pyaudio object
            stream.stop_stream()
            stream.close()
            p.terminate()

    # Close the log file
    log_file.close()

    # Restore sys.stdout to its original value if necessary
    sys.stdout = sys.__stdout__


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


# Convert "HH:MM:SS" to seconds for use with record function
def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 3600 + minutes * 60 + seconds


if __name__ == "__main__":
    # Create an argument parser
    # To use: python pyaud.py --flag

    parser = argparse.ArgumentParser(description="List input audio devices, record audio, and play back audio.")
    parser.add_argument("--list-devices", action="store_true", help="List available input audio devices")
    parser.add_argument("--record", action="store_true", help="Record audio for 30 seconds")
    parser.add_argument("--device", type=int, help="Specify the input audio device index for recording [int]")
    parser.add_argument("--play", help="Path to the audio file for playback")

    # Recording Parameters
    parser.add_argument("-d", "--duration", type=int, help="Specify the number of seconds to record (default is 10 seconds)")
    parser.add_argument("-r", "--rate", type=int, help="Specify Sampling Rate (hz) (default is 48000 hz)")

    # Optional argument for specifying a JSON file with additional parameters
    parser.add_argument("-p", "--parameters", help="Path to a JSON file with additional parameters")

    # Parse command line arguments
    args = parser.parse_args()

    if args.list_devices:
        list_audio_devices()

    elif args.record:

        # If a JSON file is provided, load the parameters
        if args.parameters:
            with open(args.parameters, 'r') as json_file:
                additional_params = json.load(json_file)

            # Merge additional parameters with the command line arguments
            args.__dict__.update(additional_params)
            record_audio(device_index=args.device, duration=time_to_seconds(args.duration), start_time=args.start_time, end_time=args.end_time, period=args.period, sample_rate=args.sample_rate, location=args.location)

        elif args.device is not None:
            record_audio(device_index=args.device - 1, duration=args.duration, sample_rate=args.rate)

        else:
            print("Please specify the input audio device index using the --device option or a file with configured parameters using -p.")

    elif args.play:
        play_audio(args.play)

    else:
        print("No action specified. Use --help to list available commands")
