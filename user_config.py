#!/usr/bin/python3.9

"""
This script takes in user input in order to specify recording
parameters for pyaud.py. These params are stored in the json
file config.json.
"""

import sys
import json
import datetime
from datetime import datetime, timedelta
from pyaud import list_audio_devices


# Input validation to ensure user input is integer
def is_int(user_input):
    try:
        int(user_input)
        return True
    except ValueError:
        print("\nPlease enter a valid integer!\n")
        return False


# Input validation to ensure user input is in range of available choices
def is_in_range(user_input, choices):
    if 0 < user_input <= choices:
        return True
    else:
        print(f"\nPlease enter enter an integer between 1 and {choices}")
        return False


# Ensures proper formatting of date_time entered by user
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


# Ensures proper formatting of time entered by user
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


# Ensures user enters an end_time that is after the start time
def end_time_after(end_time, start_time):
    end_datetime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    if end_datetime > start_datetime:
        return True
    else:
        print(f'\nError! end_time ({end_time}) must be after start_time ({start_time})\n')
        return False


# Ensures period is at least three seconds more than duration to allow time to write to .wav file
# Ensures that recoding sessions do not overlap each other.
def valid_period(period, duration):
    period_datetime = datetime.strptime(period, "%H:%M:%S").time()
    duration_datetime = datetime.strptime(duration, "%H:%M:%S").time()

    period_date = datetime.combine(datetime.today(), period_datetime)
    duration_date = datetime.combine(datetime.today(), duration_datetime)

    if (period_date - duration_date).total_seconds() < 3:
        print(f'\nPeriod ({period}) must be at least be three seconds longer than duration ({duration})!\n')
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
        user_choice = input()

        if not is_int(user_choice):
            continue

        if not is_in_range(int(user_choice), num_choices):
            continue
        else:
            user_choice = int(user_choice)
            if user_choice == 1:
                return 44_100
            elif user_choice == 2:
                return 48_000
            elif user_choice == 3:
                return 88_200
            elif user_choice == 4:
                return 96_000


def set_duration():
    while 1:
        num_choices = 3

        print("Choose a duration:")
        print("   [1] - 20 seconds")
        print("   [2] - 10 minutes")
        print("   [3] - Specify hour, minute, and second")
        user_choice = input()

        if not is_int(user_choice):
            continue

        if not is_in_range(int(user_choice), num_choices):
            continue
        else:
            user_choice = int(user_choice)

            if user_choice == 1:
                duration = "00:00:20"
                break
            elif user_choice == 2:
                duration = "00:10:00"
                break
            else:
                # Validate duration and ensure it is more than 5 seconds
                duration = valid_time()
                duration_time_object = datetime.strptime(duration, "%H:%M:%S").time()

                # Duration must be at least 5 seconds
                total_seconds = (duration_time_object.hour * 3600 +
                                 duration_time_object.minute * 60 +
                                 duration_time_object.second)

                if total_seconds < 5:
                    print("Invalid time. Duration must be more than 5 seconds!\n")
                    continue

                break

    return duration


def set_period(duration):
    while 1:
        num_choices = 4

        print("Choose period between recordings:")
        print("   [1] - 15 seconds")
        print("   [2] - 10 minutes")
        print("   [3] - 1 hour")
        print("   [4] - Specify hour, minute, and second")

        user_choice = input()

        if not is_int(user_choice):
            continue
        if not is_in_range(int(user_choice), num_choices):
            continue

        else:
            user_choice = int(user_choice)

            if user_choice == 1:
                period = "00:00:15"
            elif user_choice == 2:
                period = "00:10:00"
            elif user_choice == 3:
                period = "01:00:00"
            else:
                period = valid_time()
            if not valid_period(period, duration):
                continue
            break

    return period


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
        user_choice = input()

        if not is_int(user_choice):
            continue

        if not is_in_range(int(user_choice), num_choices):
            continue
        else:
            user_choice = int(user_choice)

            # Grabs current time for efficient time delta calculation
            current_time = datetime.now()

            if user_choice == 1:
                one_hour_later = current_time + timedelta(hours=1)
                start_time = one_hour_later.strftime('%Y-%m-%d %H:%M:%S')
            elif user_choice == 2:
                two_hours_later = current_time + timedelta(hours=2)
                start_time = two_hours_later.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_time = valid_datetime()
            break

    return start_time


def set_end_time(start_time):
    # Input end time
    start_datetime_combined = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

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
                if not end_time_after(end_time, start_time):
                    continue
            break

    return end_time


def set_recording_device():
    print("Choose a recording device:\n")
    num_choices = list_audio_devices()

    if num_choices == 0:
        print("No input devices found, terminating program.")
        sys.exit(1)

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


def set_location():
    while 1:
        print("Enter a location using 8 characters or less:")

        user_input = input()
        if len(user_input) > 8:
            print("\nError! Too many characters entered!\n")
        else:
            return user_input


def verify_config(config):
    verified = False

    while not verified:

        print("\n-----------------------------------------------------------")
        print("Are the following recording parameters correct: ")
        print(f'Sample rate: {config["sample_rate"]} kHz')
        print(f'Duration: {config["duration"]}')
        print(f'Period: {config["period"]}')
        print(f'Start Time: {config["start_time"]}')
        print(f'End Time: {config["end_time"]}')
        print(f'Recording Device: {config["device"]} - {list_audio_devices(config["device"], return_name=True)}')
        print(f'Location: {config["location"]}')

        print("\n[1] - Yes")
        print("[2] - No")

        num_choices = 2

        while 1:
            user_choice = input()

            if not is_int(user_choice):
                continue

            if not is_in_range(int(user_choice), num_choices):
                continue

            else:
                user_choice = int(user_choice)
                break

        if user_choice == 1:
            verified = True
            continue
        else:
            num_choices = 7
            print("\nWhich Parameter would you like to change: ")
            print("   [1] - Sample Rate")
            print("   [2] - Duration")
            print("   [3] - Period")
            print("   [4] - Start Time")
            print("   [5] - End Time")
            print("   [6] - Device")
            print("   [7] - Location")

            user_choice = None

            while 1:

                # user_choice may be set below to integer 2 or 4 if user specifies an invalid duration or start_time
                if user_choice is None:
                    user_choice = input()

                if not is_int(user_choice):
                    user_choice = None
                    continue

                if not is_in_range(int(user_choice), num_choices):
                    user_choice = None
                    continue

                else:
                    user_choice = int(user_choice)

                    if user_choice == 1:
                        config["sample_rate"] = set_sample_rate()
                    elif user_choice == 2:
                        config["duration"] = set_duration()
                        if not valid_period(config["period"], config["duration"]):
                            user_choice = 2
                            continue
                    elif user_choice == 3:
                        config["period"] = set_period(config["duration"])
                    elif user_choice == 4:
                        config["start_time"] = set_start_time()
                        if not end_time_after(config["end_time"], config["start_time"]):
                            user_choice = 4
                            continue
                    elif user_choice == 5:
                        config["end_time"] = set_end_time(config["start_time"])
                    elif user_choice == 6:
                        config["device"] = set_recording_device()
                    elif user_choice == 7:
                        config["location"] = set_location()

                    break


# Main

# When Python encounters an import statement, it will execute the entire script to load the module and then search for the specified attribute within it.
# Use if __name__ == "__main__": to ensure script only runs if user_config.py is explicitly ran by the user
if __name__ == "__main__":
    # Define config dictionary using user input
    sample_rate = set_sample_rate()
    duration = set_duration()
    period = set_period(duration)
    start_time = set_start_time()
    end_time = set_end_time(start_time)
    device = set_recording_device()
    location = set_location()

    config = {"sample_rate": sample_rate,
              "duration": duration,
              "period": period,
              "start_time": start_time,
              "end_time": end_time,
              "device": device,
              "index": 1,
              "location": location
              }

    verify_config(config)

    print("Dictionary created successfully: ")
    print(config)
    # Subtract 1 from device id since index in device list starts at 0
    config["device"] = config["device"] - 1
    print("Saving to config.json")

    # Convert and write JSON object to file
    with open("config.json", "w") as outfile:
        json.dump(config, outfile)
