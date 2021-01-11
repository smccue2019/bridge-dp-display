#!/bin/bash
sudo chmod 777 /sys/class/backlight/rpi_backlight/brightness
echo 150 > /sys/class/backlight/rpi_backlight/brightness
/home/pi/src/BridgeDisplay/runBridgeDisplay.py
