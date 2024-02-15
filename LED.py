#!/usr/bin/python3.9
import RPi.GPIO as GPIO
import time

#Disable GPIO warnings
GPIO.setwarnings(False)

#Sets numbering scheme to Broadcom (BCM) mode
#BCM channel numbers are consistent across different models of rasberry pi
GPIO.setmode(GPIO.BCM)

#Configures pin 18 as output
GPIO.setup(18, GPIO.OUT)

#Record the start time
start_time = time.time()

print("Executing loop")

#Executes loop for 10 seconds
#Turns Pin 18 on and off based on the sleep time
while (time.time() - start_time) < 10:
    GPIO.output(18, True)
    time.sleep(1)
    GPIO.output(18, False)
    time.sleep(1)

print("Finished")