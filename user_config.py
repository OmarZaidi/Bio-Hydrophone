#!/usr/bin/python3.9

"""
This script takes in user input in order to specify recording
parameters for pyaud.py. These params are stored in a json
file.
"""

import sys
import json
import datetime
from datetime import datetime, timedelta
from pyaud import list_audio_devices


# Input Validation
def is_int(user_input):
    try:
        int(user_input)
        return True
    except ValueError:
        print("\nPlease enter a valid integer!\n")
        return False


def is_in_range(user_input, choices):
    if 0 < user_input <= choices:
        return True
    else:
        print(f"\nPlease enter enter an integer between 1 and {choices}")
        return False


def valid_datetime():
    while 1:
        print("Enter datetime in following format: YYYY-MM-DD HH:MM:SS")
        user_input = input()

        try:
            # Parse the user input into a datetime object
            user_datetime = datetime.strptime(user_input, '%Y-%m-%d %H:%M:%S')
            # Convert the datetime object back to a string so that it can be stored in JSON file
            return user_datetime.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            print("\nPlease enter a valid datetime!\n")


# Returns string
def valid_time():
    while 1:
        print("Enter time in following format: HH:MM:SS")
        user_input = input()

        try:
            # Parse the user input into a datetime object
            user_datetime = datetime.strptime(user_input, '%H:%M:%S')
            # Convert the time object back to a string so that it can be stored in JSON file
            return user_datetime.strftime('%H:%M:%S')
        except ValueError:
            print("\nPlease enter a valid time!\n")


def valid_time_delta(time_delta, duration):
    time_delta = datetime.strptime(time_delta, "%H:%M:%S").time()
    duration = datetime.strptime(duration, "%H:%M:%S").time()

    time_delta_date = datetime.combine(datetime.today(), time_delta)
    duration_date = datetime.combine(datetime.today(), duration)

    if (time_delta_date - duration_date).total_seconds() < 3:
        print("\nBuffer time must at least be three seconds longer than duration!\n")
        return False
    else:
        return True


# Input sample rate
def set_sample_rate():
    while 1:
        num_choices = 4

        print("Choose sample rate:")
        print("   [1] - 44.1 kHz")
        print("   [2] - 48 kHz")
        print("   [3] - 88.2 kHz")
        print("   [4] - 96 kHz")
        sample_rate = input()

        if not is_int(sample_rate):
            continue

        if not is_in_range(int(sample_rate), num_choices):
            continue
        else:
            sample_rate = int(sample_rate)
            if sample_rate == 1:
                return 44_100
            elif sample_rate == 2:
                return 48_000
            elif sample_rate == 3:
                return 88_200
            elif sample_rate == 4:
                return 96_000


def set_duration():
    while 1:
        num_choices = 3

        print("Choose a duration:")
        print("   [1] - 20 seconds")
        print("   [2] - 10 minutes")
        print("   [3] - Specify hour, minute, and second")
        duration = input()

        if not is_int(duration):
            continue

        if not is_in_range(int(duration), num_choices):
            continue
        else:
            duration = int(duration)

            if duration == 1:
                duration = "00:00:20"
                break
            elif duration == 2:
                duration = "00:10:00"
                break
            else:
                duration = valid_time()
                duration_time_object = datetime.strptime(duration, "%H:%M:%S").time()

                # Duration must be at least 5 seconds
                if duration_time_object.second < 5:
                    print("Invalid time. Duration must be more than 5 seconds!\n")
                    continue

                break

    return duration


def set_buffer_time(duration):
    while 1:
        num_choices = 4

        print("Choose period between recordings:")
        print("   [1] - 15 seconds")
        print("   [2] - 10 minutes")
        print("   [3] - 1 hour")
        print("   [4] - Specify hour, minute, and second")

        delta_time = input()

        if not is_int(delta_time):
            continue
        if not is_in_range(int(delta_time), num_choices):
            continue

        else:
            delta_time = int(delta_time)

            if delta_time == 1:
                delta_time = "00:00:20"
            elif delta_time == 2:
                delta_time = "00:10:00"
            elif delta_time == 3:
                delta_time = "01:00:00"
            else:
                delta_time = valid_time()
            if not valid_time_delta(delta_time, duration):
                continue
            break

    return delta_time


# Allows user to specify time to start recording
# Params: None
# Returns: String: time set by user

def set_start_time():
    # Input Start Time
    while 1:
        num_choices = 3

        print("Choose start time:")
        print("   [1] - 1 hour from now")
        print("   [2] - 2 hours from now")
        print("   [3] - Specify date and time")
        start_time = input()

        if not is_int(start_time):
            continue

        if not is_in_range(int(start_time), num_choices):
            continue
        else:
            start_time = int(start_time)

            # Grabs current time for efficient time delta calculation
            current_time = datetime.now()

            if start_time == 1:
                one_hour_later = current_time + timedelta(hours=1)
                start_time = one_hour_later.strftime('%Y-%m-%d %H:%M:%S')
            elif start_time == 2:
                two_hours_later = current_time + timedelta(hours=2)
                start_time = two_hours_later.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_time = valid_datetime()
            break

    return start_time


def set_end_time(start_datetime_combined):
    # Input end time
    start_datetime_combined = datetime.strptime(start_datetime_combined, '%Y-%m-%d %H:%M:%S')

    while 1:
        num_choices = 3

        print("Choose end time:")
        print("   [1] - 1 hour after first recording")
        print("   [2] - 2 hours after first recording")
        print("   [3] - Specify date and time")
        user_choice = input()

        if not is_int(user_choice):
            continue

        if not is_in_range(int(user_choice), num_choices):
            continue
        else:
            user_choice = int(user_choice)

            if user_choice == 1:
                one_hour_later = start_datetime_combined + timedelta(hours=1)
                end_time = one_hour_later.strftime('%Y-%m-%d %H:%M:%S')
            elif user_choice == 2:
                two_hours_later = start_datetime_combined + timedelta(hours=2)
                end_time = two_hours_later.strftime('%Y-%m-%d %H:%M:%S')
            else:
                end_time = valid_datetime()

            break

    return end_time


def set_recording_device():
    print("Choose a recording device:\n")
    num_choices = list_audio_devices()

    if num_choices == 0:
        print("No input devices found, terminating program.")
        sys.exit

    while 1:
        user_choice = input()

        if not is_int(user_choice):
            continue

        if not is_in_range(int(user_choice), num_choices):
            continue

        else:
            device = int(user_choice)
            break

    return device


# Main

# Define config dictionary using user input

sample_rate = set_sample_rate()
duration = set_duration()
time_delta = set_buffer_time(duration)
start_time = set_start_time()
end_time = set_end_time(start_time)
device = set_recording_device()

config = {"sample_rate": sample_rate,
          "duration": duration,
          "delta_time": time_delta,
          "start_time": start_time,
          "end_time": end_time,
          "device": device,
          "index": 1
          }
print("Dictionary created successfully: ")
print(config)
print("Saving to config.json")

# Convert and write JSON object to file
with open("config.json", "w") as outfile:
    json.dump(config, outfile)
