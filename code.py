# Pi Pico Firefly Simulator With Sleep and Daytime Sensing
# 5v Solar Panel has a photoresistor on ADC0 to sense daylight levels
# https://github.com/Crysknife007/firefly - Spike Snell 2024

# Import what we need to run the firefly
import time, board, pwmio, random, microcontroller, alarm

# Import AnalogIn for the ADC
from analogio import AnalogIn

# ----------- Configuration Options -------------------------------.
                                                                   #
# Initialize the duskThreshold                                     #
duskThreshold = 1200                                               #
                                                                   #
# Set the number of blinks we should have for a single firefly     #
numberOfBlinks = 1000                                              #
                                                                   #
# Initialize the polling interval in seconds                       #
pollingInterval = 1800                                             #
                                                                   #
# Define the minimum time between blinks                           #
minimumBlinkInterval = 3                                           #
                                                                   #
# Define the maximum time between blinks                           #
maximumBlinkInterval = 14                                          #
                                                                   #
# Initialize the daylight count needed to trigger a blink cycle    #
daylightCountNeeded = 3                                            #
                                                                   #
# Define which LED to use                                          #
ledPin = board.GP15 # board.LED is the built-in LED                #
                                                                   #
# -----------------------------------------------------------------'

# Set up the ADC
adc = AnalogIn( board.A0 )

# Create a pseudorandom frequency
freq = random.randint( 2000, 200000 )

# Set up the LED
led = pwmio.PWMOut( ledPin, frequency = freq, duty_cycle = 0 )

# Initialize the daylight counter
daylightCount = 0

# Set up the firefly blink loop
def runFirefly():
        
    # Loop a lot of times to act as an individual firefly
    for i in range( numberOfBlinks ):

        # Ramp the brightness up somewhat quickly 
        for b in range( 6553 ):       
   
            # Set the led brightness
            led.duty_cycle = b * 10

        # Fade the led out more slowly
        for f in range( 65535 ):

            # Set the led brightness
            led.duty_cycle = 65535 - f

        # Light sleep for an amount of time between minimumBlinkInterval and maximumBlinkInterval
        lightSleep( random.randint( minimumBlinkInterval, maximumBlinkInterval ) )

# Define the light sleep function
def lightSleep( sleepDuration ):

    # Define an alarm for an amount of time between minimumBlinkInterval and maximumBlinkInterval
    time_alarm = alarm.time.TimeAlarm( monotonic_time = time.monotonic() + sleepDuration )

    # Do a light sleep until the alarm wakes us.
    alarm.light_sleep_until_alarms( time_alarm )

# Define the deep sleep function
def deepSleep( sleepDuration ):

    # Create an alarm to deep sleep until
    time_alarm = alarm.time.TimeAlarm( monotonic_time = time.monotonic() + sleepDuration )

    # Exit the program, and then deep sleep until the alarm wakes us.
    alarm.exit_and_deep_sleep_until_alarms( time_alarm ) 

# Get the adc value
adcValue = adc.value;

# If it is currently daylight, blink the startup indication light
if ( adcValue < duskThreshold ):  

    # Turn on the LED
    led.duty_cycle = 65535

    # Light sleep for half a second
    lightSleep( .5 )

    # Turn off the LED
    led.duty_cycle = 0 

# Loop for as long as the firefly lives
while True:

    # Get the adc value
    adcValue = adc.value;

    # If it is not daytime, and the daylight count is sufficient, then blink the light
    if adcValue > duskThreshold and daylightCount >= daylightCountNeeded:

        # Run the firefly blink loop
        runFirefly()

        # Deep sleep until the next polling interval ( This resets the daylight count as well )
        deepSleep( pollingInterval )

    # Else if we haven't seen enough daylight counts to blink
    elif adcValue > duskThreshold:

        # Light sleep for 3 seconds ( Without this I have been running into issues. )
        lightSleep( 3 )

        # Deep sleep for one polling interval ( This resets the daylight count as well )
        deepSleep( pollingInterval )

    # Else if it is daytime
    elif adcValue < duskThreshold:

        # Increment the daylight count
        daylightCount += 1

        # Light sleep for as long as our polling interval
        lightSleep( pollingInterval )
