from GlobalConfiguration import GlobalConfiguration
import serial
import time
import json
import random
from WifiBulb import WifiBulb
from SerialLightController import SerialLightController

# dono't actually do anything
dryRun = True

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
stripWidth = 0

# patio lights main script
config = GlobalConfiguration("configuration.ini")

# should handle the lightbulb pattern stuff somewhere else

def pulse(color1, color2, delay):
    global dryRun
    time.sleep(delay / 1000.0)
    if not dryRun:
        bulb1.setColor(color1)
        bulb2.setColor(color1)
        bulb3.setColor(color1)
    else:
        print("set bulb color: ", color1)
    time.sleep(delay / 1000.0)
    if not dryRun:
        bulb1.setColor(color2)
        bulb2.setColor(color2)
        bulb3.setColor(color2)
    else:
        print("set bulb color: ", color2)


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
    global stripWidth
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
        stripWidth = jsonData["width"]
        file.close()
        print("got data from file")
    except FileNotFoundError:
        print("Data file not found, check configuration.ini")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("Start of program")
    print(dryRun)
    config = GlobalConfiguration("configuration.ini")
    config.load()
    # configuration loaded
    # open serial connection
    serLights = SerialLightController(config)
    serLights.connect()
    
    # open data file, parse it, close it
    readWebColorData()

    bulb1 = WifiBulb(config.Lightbulb1_IP)
    bulb2 = WifiBulb(config.Lightbulb2_IP)
    bulb3 = WifiBulb(config.Lightbulb3_IP)

    try:
        if not dryRun:
            bulb1.connect()
            bulb2.connect()
            bulb3.connect()
        x = 1 # nothing
    except Exception as e:
        print("Failed to connect to one or more lightbulbs! " + str(e))

    try:
        if not dryRun:
            bulb1.setColor(bulbColor1)
            bulb2.setColor(bulbColor1)
            bulb3.setColor(bulbColor1)
        else:
            print("all bulbs set to ", bulbColor1)
        delay = 1
        longerDelay = 0.5
        
        #serLights.setPatternAndColors('2', (255,0,0), (0,0,0), 500,0)
        #command = serLights.getJSONStr('2', (255, 0,0), (0,0,0), 500, 500)

        #if not dryRun:
        #    serLights.sendMessage(command)
        #else:
        #    print("Serial: " + command)

        while(True):
            # test command, this works
            #command = 'start225500025500000000005000500end\n'

            #command = serLights.getSerialString('2', (255,0,0), (0,0,0), 500, 500)
            #print(command)
            #serLights.sendMessage(command)
            #c = ( random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            #serLights.setPatternAndColors('3', c, (0,0,0), 100, 100, 15)

            # read the contents of the file again
            readWebColorData()
            serLights.setPatternAndColors(stripPattern, stripColor1, stripColor2, stripDelay1, stripDelay1, stripWidth)
            # sleep for a little bit
            time.sleep(0.5)
            # keep the lights on for a few seconds
            #placeholder pattern, just turn the lights on and off in a pulsing pattern
            if not dryRun:
                pulse(bulbColor1, bulbColor2, delay)
            else:
                print("pulse " , bulbColor1)
    except(KeyboardInterrupt, SystemExit):
        print("End of program")
        # disconnect from everything
        bulb1.disconnect()
        bulb2.disconnect()
        bulb3.disconnect()
        serLights.disconnect()
        print("end")
        #turn everything off
