#!/bin/sh
# launcher.sh
# navigate to home, then to test directory, then execute python script, then back home

cd /
cd home/uhalpern/test
sudo python pyaud.py --record --device=1 -p .\config.json
cd /