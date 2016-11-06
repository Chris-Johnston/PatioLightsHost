from GlobalConfiguration import GlobalConfiguration
import serial
import time
import json
#import random
from WifiBulb import WifiBulb
from SerialLightController import SerialLightController

ser = serial.Serial()

# data
bulbColor1 = (0,0,0)
bulbColor2 = (0,0,0)
bulbColor3 = (0,0,0)
bulbDelay1 = 999
bulbPattern = 0

stripColor1 = (0,0,0)
stripColor2 = (0,0,0)
stripDelay1 = 750
stripPattern = 0

# patio lights main script
config = GlobalConfiguration("configuration.ini")

# should handle the lightbulb pattern stuff somewhere else

def pulse(color1, color2, delay):
    time.sleep(delay / 1000.0)
    bulb1.setColor(color1)
    bulb2.setColor(color1)
    bulb3.setColor(color1)
    time.sleep(delay / 1000.0)
    bulb1.setColor(color2)
    bulb2.setColor(color2)
    bulb3.setColor(color2)


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

def readWebColorData():
    global bulbColor1
    global bulbColor2
    global bulbColor3
    global bulbDelay1
    global bulbPattern
    global stripColor1
    global stripColor2
    global stripDelay1
    global stripPattern
    try:
        print(config.DataFile)
        file = open(config.DataFile, "r")
        
        jsonData = json.load(file)
        # read data and update it
        bulbColor1 = jsonData["bulbColor1"]
        bulbColor2 = jsonData["bulbColor2"]
        bulbColor3 = jsonData["bulbColor3"]
        bulbDelay1 = int(jsonData["bulbDelay1"])
        bulbPattern = jsonData["bulbPattern"]

        stripColor1 = jsonData["stripColor1"]
        stripColor2 = jsonData["stripColor2"]
        stripDelay1 = int(jsonData["stripDelay1"])
        stripPattern = jsonData["stripPattern"]
        file.close()
        print("got data from file")
    except FileNotFoundError:
        print("Data file not found, check configuration.ini")


if __name__ == "__main__":
    print("Start of program")
    config = GlobalConfiguration("configuration.ini")
    config.load()
    # configuration loaded
    # open serial connection
    serLights = SerialLightController("configuration.ini")
    #serLights.connect()
    
    # open data file, parse it, close it
    readWebColorData()

    bulb1 = WifiBulb(config.Lightbulb1_IP)
    bulb2 = WifiBulb(config.Lightbulb2_IP)
    bulb3 = WifiBulb(config.Lightbulb3_IP)

    try:
        #bulb1.connect()
        #bulb2.connect()
        #bulb3.connect()
        x = 1 # nothing
    except Exception as e:
        print("Failed to connect to one or more lightbulbs! " + str(e))

    try:
        
        #bulb1.setColor(color1)
        #bulb2.setColor(color1)
        #bulb3.setColor(color1)
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
            #cycleLights(bulbColor1, bulbColor2, longerDelay, delay)
    except(KeyboardInterrupt, SystemExit):
        print("End of program")
        # turn off the bulbs
        bulb1.disconnect()
        bulb2.disconnect()
        bulb3.disconnect()
        serLights.disconnect()
        print("end")
        #turn everything off
