# Bio-Hydrophone Project: pyaud.py Overview

## Introduction
The `pyaud.py` script in the Bio-Hydrophone repository is a versatile tool designed for audio recording and playback, tailored for bioacoustic research using hydrophones. Leveraging the `pyaudio` library, this script facilitates easy interaction with audio devices for recording and analyzing underwater sounds.

## Features
- **List Audio Devices**: Easily identify and select audio devices connected to your system for recording.
- **Audio Recording**: Customizable audio recording settings, including device selection, recording duration, and sample rate, to capture high-quality audio data.
- **Audio Playback**: Play back recorded audio files for analysis and review of captured sounds.

## Getting Started

### Prerequisites
- Python 3.9 or later
- pyaudio library

### Installation
1. Ensure Python and pip are installed on your system.
2. Install `pyaudio` using pip:
   ```
   pip install pyaudio
   ```
   On Linux, you may need to install additional dependencies:
   ```
   sudo apt-get install portaudio19-dev
   ```

### Usage
- **Listing Audio Devices**:
  ```
  python pyaud.py --list-devices
  ```
- **Recording Audio**:
  Specify the device index, duration (in seconds), and output directory:
  ```
  python pyaud.py --record --device <device_index> --duration <duration_in_seconds> --output-directory <output_path>
  ```
- **Playing Audio**:
  Provide the path to the audio file you wish to play:
  ```
  python pyaud.py --play <path_to_audio_file>
  ```

## Contributing
We welcome contributions to the `pyaud.py` script and the broader Bio-Hydrophone project. Whether it's adding new features, improving documentation, or reporting bugs, your input is valuable in enhancing this tool for bioacoustic research.
