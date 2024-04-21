# Firefly
A solar powered firefly in CircuitPython designed for the Pi Pico

The onboard LED on the pico is used to emulate a firefly by smoothly pulsating in a natural way. 

A voltage divider is used to read the daylight amount directly from the solar panel. 
Two 10k resistors are used in my approach, but other similar values would work.

The board sleeps most of the time, using deep sleep when it can ( Most of the night. ) and light sleep the rest of the time.

A daylight counter is used, so that the firefly has to experience a number of valid daylight readings in a row in order to start a blink cycle. 
This is so that the firefly can start around dusk, and then blink for perhaps a few hours, and then stop blinking for the rest of the night. 
It saves power to behave this way, and also is more like what a real firefly would do compared to blinking all night. 

The polling rate, and all other settings are configurable near the top of the code.
