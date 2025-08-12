from gpiozero import PWMOutputDevice
from time import sleep

fan = PWMOutputDevice(14, active_high=True, initial_value=0, frequency=1000)

try:
    for duty in [0, 0.2, 0.5, 0.8, 1.0]:
        print(f"Setting duty cycle to: {duty*100:.0f}%")
        fan.value = duty
        sleep(3)
except KeyboardInterrupt:
    pass
finally:
    fan.close()
