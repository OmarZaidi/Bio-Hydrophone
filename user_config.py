#!/usr/bin/python3.9

"""
This script takes in user input in order to specify recording
parameters for pyaud.py. These params are stored in a json
file.
"""

import json
import datetime
from datetime import datetime, timedelta


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
        print("   [3] - Specify hour and minute")
        duration = input()

        if not is_int(duration):
            continue

        if not is_in_range(int(duration), num_choices):
            continue
        else:
            duration = int(duration)
            current_time = datetime.now()

            if duration == 1:
                duration = "00:00:20"
            elif duration == 2:
                duration = "00:10:20"
            else:
                duration = valid_time()
            break

    return str(duration)


# Allows user to specify time to start recording
# Params: None
# Returns: String: time set by user
def valid_time():
    while 1:
        print("Enter start time in following format: HH:MM:SS")
        user_input = input()

        try:
            # Attempt to parse input time
            user_time = datetime.strptime(user_input, '%H:%M:%S').time()
            return user_time.strftime('%H:%M:%S')
        except ValueError:
            print("\nPlease enter a valid time!\n")


def set_start_time():
    # Input Start Time
    while 1:
        num_choices = 3

        print("Choose start time:")
        print("   [1] - 1 hour from now")
        print("   [2] - 2 hours from now")
        print("   [3] - Specify hour and minute")
        start_time = input()

        if not is_int(start_time):
            continue

        if not is_in_range(int(start_time), num_choices):
            continue
        else:
            start_time = int(start_time)
            current_time = datetime.now()

            if start_time == 1:
                one_hour_later = current_time + timedelta(hours=1)
                start_time = one_hour_later.strftime('%H:%M:%S')
            elif start_time == 2:
                two_hours_later = current_time + timedelta(hours=2)
                start_time = two_hours_later.strftime('%H:%M:%S')
            else:
                start_time = valid_time()
            break

    return str(start_time)


# Main

# Define config dictionary using user input
config = {"sample_rate": set_sample_rate(),
          "duration": set_duration(),
          "start_time": set_start_time()
          }
print("Dictionary created successfully: ")
print(config)
print("Saving to config.json")

# Convert and write JSON object to file
with open("config.json", "w") as outfile:
    json.dump(config, outfile)
