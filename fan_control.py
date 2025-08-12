#!/usr/bin/env python3
from gpiozero import PWMOutputDevice
from time import sleep
import os


# Pin config
FAN_PIN = 14  # BCM numbering
FREQ = 20

# Temperature thresholds (°C)
TEMP_MIN = 45  # Fan off below this temp
TEMP_MAX = 80  # Fan 100% above this temp

# Check every CHECK_INTERVAL seconds
CHECK_INTERVAL = 5

# Override file for manual control
OVERRIDE_FILE = "/tmp/fan_override" # Contents: "auto", "on", "off", or duty % (0-100)

# Current file status is written here and can be read by the user
FAN_STATUS_FILE = "/tmp/fan_status"


def get_cpu_temp():
    """Read CPU temperature in °C."""
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return int(f.read()) / 1000


def calc_duty_cycle(temp):
    """
    Map temperature to duty cycle (0.0 - 1.0).
    Linear between TEMP_MIN and TEMP_MAX.
    """
    if temp <= TEMP_MIN:
        return 0.0
    elif temp >= TEMP_MAX:
        return 1.0
    else:
        return (temp - TEMP_MIN) / (TEMP_MAX - TEMP_MIN)


def read_override():
    """Read override state from file."""
    if not os.path.exists(OVERRIDE_FILE):
        return "auto"
    try:
        with open(OVERRIDE_FILE, "r") as f:
            return f.read().strip().lower()
    except:
        return "auto"
    

def get_duty_cycle(mode, temp):
    """
    Get the duty cycle for a given mode and temperature.

    Mode should be read from a configuration file using read_override().
    Can be "auto", "on" (maps to 1.0), "off" (maps to 0.0) or a number.
    If set to "auto", it is calculated using calc_duty_cycle() function.
    """
    if mode == "on":
        return 1.0
    elif mode == "off":
        return 0.0
    elif mode.replace(".", "", 1).isdigit():
        percent = float(mode)
        return max(0.0, min(1.0, percent / 100))
    else: # "auto"
        return calc_duty_cycle(temp)
    

def log_status(temp, mode, duty):
    """Writes the current state to a file"""
    if mode.replace(".", "", 1).isdigit():
        mode = "manual"
    with open(FAN_STATUS_FILE, "w") as status_file:
        status_file.write(f"Temp: {temp}°C | Fan: {duty*100:.0f}% | Mode: {mode}\n")


def main():
    fan = PWMOutputDevice(FAN_PIN, active_high=True, initial_value=0, frequency=FREQ)

    try:
        while True:
            temp = get_cpu_temp()
            mode = read_override()
            duty = get_duty_cycle(mode, temp)
            fan.value = duty
            log_status(temp, mode, duty)
            sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        pass
    finally:
        fan.close()


if __name__ == "__main__":
    main()
