# Firefly
A solar powered firefly in CircuitPython designed for the Pi Pico

A yellow-green led is used to emulate a firefly by smoothly pulsating in a natural way. 
If using an original pico, the board.LED works well for this. If using a clone board with a less pleasant led a custom one can be used.

A 5516 5-10k photoresistor is used to determine the amount of daylight. It is connected to ADC0
My original approach used a voltage divider but this needed to be dialed in each time.
With the photoresistor there is a standard baseline to work with so there is less tweaking

The board sleeps most of the time, waking up only to blink and check for the amount of daylight.

A daylight counter is used, so that the firefly has to experience a number of valid daylight readings in a row in order to start a blink cycle. 
This is so that the firefly can start around dusk, and then blink for perhaps a few hours, and then stop blinking for the rest of the night. 
It saves power to behave this way, and also is more like what a real firefly would do compared to blinking all night. 

The polling rate, and all other settings are configurable near the top of the code.

This is tuned for the 7.3.3 CircuitPython firmware, newer ones will work, but they don't perform in exactly the same way. They added a blinking startup flash to the onboard LED in newer versions, and appear to have increased the clock speed. So 7.3.3 is included in this repository for my own convenience. 
