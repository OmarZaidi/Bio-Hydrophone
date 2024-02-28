
# Bio-Hydrophone Project: pyaud.py Overview

## Introduction
The `pyaud.py` script is an integral part of the Bio-Hydrophone project, designed to facilitate audio recording and playback for bioacoustic research. This Python-based tool leverages the `pyaudio` library to interface with audio hardware, enabling users to record and analyze underwater sounds or any audio data captured through hydrophones or microphones.

## Detailed Script Overview

### Dependencies
- **Python 3.9**: Target version for compatibility and performance.
- **PyAudio**: For accessing audio streams directly from the hardware.
- **Argparse**: For parsing command-line arguments.
- **Wave**: For reading and writing WAV files, facilitating audio data manipulation.
- **Datetime**, **Time**, **OS**, **JSON**: For handling timing functions, file system interactions, and configuration settings.

### Features

#### 1. **Listing Audio Devices**
The `list_audio_devices()` function scans and lists all available audio devices with input capabilities, aiding in the selection of the correct device for recording.

#### 2. **Recording Audio**
The `record_audio()` function allows for recording audio with customizable settings such as device index, duration, start time, sample rate, and output directory. It supports delayed recording to start at a specific time and saves the audio in WAV format.

#### 3. **Playing Audio**
The `play_audio()` function plays back WAV audio files through the system's output devices, enabling users to review recorded audio files.

### Usage
The script is designed for command-line execution with various flags for different functionalities:

- `--list-devices`: Lists all detected audio input devices.
- `--record`: Starts recording audio. Can be customized with `--device`, `--duration`, and `--parameters` flags for device selection, recording duration, and additional parameters via a JSON file, respectively.
- `--play`: Plays a specified WAV file.

### Configuration via JSON
An optional `--parameters` flag allows specifying a JSON file with additional recording settings, offering an extensible and user-friendly way to adjust recording parameters without modifying the script code.

### Example Commands
- **Listing Audio Devices**
  ```
  python pyaud.py --list-devices
  ```
- **Recording Audio**
  ```
  python pyaud.py --record --device 1 --duration 10
  ```
- **Playing Back Audio**
  ```
  python pyaud.py --play ./recordings/my_audio.wav
  ```

## Contributing
Contributions to the `pyaud.py` script and the Bio-Hydrophone project are highly appreciated. Whether it's feature enhancements, bug reports, or documentation improvements, your input helps make this tool more effective for bioacoustic research and related fields.

## License
N/A
