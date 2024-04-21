# Pi Pico Firefly Simulator With Sleep and Daytime Sensing
# 5v Solar Panel has a voltage divider of two 10k resistors.
# The divided voltage is sent to ADC0 on the pico for light sensing
# By Spike Snell 2024

# Import what we need to run the onboard led
import time, board, pwmio, random, microcontroller, alarm

# Import AnalogIn for the ADC
from analogio import AnalogIn

# Initialize the duskThreshold
duskThreshold = 500

# Set the number of blinks we should have for a single firefly
numberOfBlinks = 1000

# Initialize the polling interval in seconds
pollingInterval = 1800

# Define the minimum time between blinks
minimumBlinkInterval = 3

# Define the maximum time between blinks
maximumBlinkInterval = 14

# Initialize the daylight count needed to trigger a blink cycle
daylightCountNeeded = 3

# Initialize the daylight counter
daylightCount = 0

# Set up the ADC
adc = AnalogIn(board.A0)

# Create a pseudorandom frequency
freq = random.randint( 2000, 200000 )

# Set up the led
led = pwmio.PWMOut( board.LED, frequency = freq, duty_cycle = 0 )

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

        # Define an alarm for an amount of time between minimumBlinkInterval and maximumBlinkInterval
        time_alarm = alarm.time.TimeAlarm( monotonic_time = time.monotonic() + random.randint( minimumBlinkInterval, maximumBlinkInterval ) )

        # Do a light sleep until the alarm wakes us.
        alarm.light_sleep_until_alarms( time_alarm )

# Loop forever
while True:

    # If it is not daytime, and the daylight count is sufficient, then blink the light
    if adc.value < duskThreshold and daylightCount >= daylightCountNeeded:

        # Set the daylight count back to 0
        daylightCount = 0

        # Run the firefly blink loop
        runFirefly()


    # Else if we haven't seen enough daylight counts to blink
    elif adc.value < duskThreshold:
        
        # Create an alarm to deep sleep until
        time_alarm = alarm.time.TimeAlarm( monotonic_time = time.monotonic() + pollingInterval )

        # Exit the program, and then deep sleep until the alarm wakes us.
        alarm.exit_and_deep_sleep_until_alarms( time_alarm )


    # Else it must be daytime
    else:

        # Increment the daylight count
        daylightCount += 1

        # Create an alarm to light sleep until
        time_alarm = alarm.time.TimeAlarm( monotonic_time = time.monotonic() + pollingInterval )

        # Do a light sleep until the alarm wakes us.
        alarm.light_sleep_until_alarms( time_alarm )


