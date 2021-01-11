#!/usr/bin/python
# Scott McCue WHOI NDSF Sept 2018
# Makes use of code  from bh1750.py Read data from a BH1750 digital light sensor.
# Author : Matt Hawkins https://www.raspberrypi-spy.co.uk/?s=bh1750
# Also the rpi_brightness library, author unknown.

import smbus
import time
from rpi_backlight import set_brightness

# Define some constants from the data set

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
  return convertToNumber(data)


# SJM Sept 2018 added a BH1750 light sensor, found python projects
# on interwebs.
# readLight queries the BH1750, which is attached to raspi GPIO bus.
# Bright light appears to measure at 80 and higher.
# Covering the light sensor with my hand drop measured light to a value
# below 5.
def adjust_brightness(measured_level):

  if measured_level <= 5:
    set_brightness(15,True, 3)
 
  elif measured_level <= 40 and measured_level > 5:
    set_brightness(15,True, 3)
 
  elif measured_level < 80 and measured_level > 40:
    set_brightness(75,True, 3)

  else:
    set_brightness(220, True, 3)
 #   dim_flag = False
 #   return measured_level, dim_flag
