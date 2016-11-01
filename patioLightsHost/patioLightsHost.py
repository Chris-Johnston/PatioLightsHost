from GlobalConfiguration import GlobalConfiguration
import serial
import time
#import random
from WifiBulb import WifiBulb
from SerialLightController import SerialLightController

ser = serial.Serial()
# placeholder configuration for halloween 
# patio lights main script
config = GlobalConfiguration("configuration.ini")

def cycleLights(color1, color2, longerDelay, delay):
    time.sleep(longerDelay)
    bulb1.setColor(color2)
    time.sleep(delay)
    bulb1.setColor(color1)
    bulb2.setColor(color2)
    time.sleep(delay)
    bulb2.setColor(color1)
    bulb3.setColor(color2)
    time.sleep(delay)
    bulb3.setColor(color1)


if __name__ == "__main__":
    print("Start of program")
    config = GlobalConfiguration("configuration.ini")
    config.load()
    # configuration loaded
    # open serial connection
    serLights = SerialLightController("configuration.ini")
    serLights.connect()
        
    try:
        file = open(config.DataFile, "rb")
    except FileNotFoundError:
        print("Data file not found, check configuration.ini")

    bulb1 = WifiBulb(config.Lightbulb1_IP)
    bulb2 = WifiBulb(config.Lightbulb2_IP)
    bulb3 = WifiBulb(config.Lightbulb3_IP)

    try:
        bulb1.connect()
        bulb2.connect()
        bulb3.connect()
    except Exception as e:
        print("Failed to connect to one or more lightbulbs! " + str(e))

    try:
        color1 = (255,0,0)
        color2 = (0,0,0)
        bulb1.setColor(color1)
        bulb2.setColor(color1)
        bulb3.setColor(color1)
        delay = 1
        longerDelay = 0.5
        serLights.setPatternAndColors('2', (255,0,0), (0,0,0), 500,0)

        while(True):
            # read the contents of the file again
            #try:
            #    file = open(config.DataFile, "rb")
            #except FileNotFoundError:
            #    print("Web data file not found!")
            
            # keep the lights on for a few seconds
            #placeholder pattern, just turn the lights on and off in a pulsing pattern
            cycleLights(color1, color2, longerDelay, delay)
    except(KeyboardInterrupt, SystemExit):
        print("End of program")
        # turn off the bulbs
        bulb1.disconnect()
        bulb2.disconnect()
        bulb3.disconnect()
        serLights.disconnect()
        print("end")
        #turn everything off
