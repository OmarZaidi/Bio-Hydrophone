#!/bin/sh
# launcher.sh
# navigate to home, then to test directory, then execute python script, then back home

cd /
cd home/rpi/Bio-Hydrophone
sudo python pyaud.py --record --device=1 -d 10 -r 46000
cd /