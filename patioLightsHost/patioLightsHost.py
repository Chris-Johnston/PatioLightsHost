﻿from GlobalConfiguration import GlobalConfiguration
import serial
import time
import json
import random
from WifiBulb import WifiBulb
from SerialLightController import SerialLightController


dryRun = False

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

#def pulse(color1, color2, delay):
#    global dryRun
#    time.sleep(delay / 1000.0)
#    if not dryRun:
#        bulb1.setColor(color1)
#        bulb2.setColor(color1)
#        bulb3.setColor(color1)
#    else:
#        print("set bulb color: ", color1)
#    time.sleep(delay / 1000.0)
#    if not dryRun:
#        bulb1.setColor(color2)
#        bulb2.setColor(color2)
#        bulb3.setColor(color2)
#    else:
#        print("set bulb color: ", color2)


#def cycleLights(color1, color2, longerDelay, delay):
#    time.sleep(longerDelay)
#    bulb1.setColor(color2)
#    time.sleep(delay)
#    bulb1.setColor(color1)
#    bulb2.setColor(color2)
#    time.sleep(delay)
#    bulb2.setColor(color1)
#    bulb3.setColor(color2)
#    time.sleep(delay)
#    bulb3.setColor(color1)

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
        bulbPattern = jsonData["bulddbPattern"]

        stripColor1 = jsonData["stripColor1"]
        stripColor2 = jsonData["stripColor2"]
        stripDelay1 = int(jsonData["stripDelay1"])
        stripPattern = jsonData["stripPattern"]
        stripWidth = jsonData["width"]
        file.close()
        print("got data from file")
    except OSError:
        print("Data file not found, check configuration.ini")
    except Exception as e:
        print(e)

        #todo consider adding downtimes where lights cannot be changed, or have
        # a default pattern for tduring those times
        # so I'm not strobing out at 3am

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
    except Exception as e:
        print("Failed to connect to one or more lightbulbs! " + str(e))

    try:
        if not dryRun:
            bulb1.setColor(bulbColor1)
            bulb2.setColor(bulbColor2)
            bulb3.setColor(bulbColor3)
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
        # allows everything to get ready
        #time.sleep(5)
        while(True):
            # sleep for a bit, so that I'm not constantly reading from the file
            time.sleep(5)
            # read the contents of the file again
            readWebColorData()
            # send info to serial (will automatically discard duplicates)
            serLights.setPatternAndColors(stripPattern, stripColor1, stripColor2, stripDelay1, stripDelay1, stripWidth)

            # determine which lightbulb pattern to use
            if(bulbPattern == config.bulbPatternsDict.get('pattern_bulb_color1')):
                bulb1.setColor(bulbColor1)
                bulb2.setColor(bulbColor1)
                bulb3.setColor(bulbColor1)
            elif(bulbPattern == config.bulbPatternsDict.get('pattern_bulb_coloreach')):
                bulb1.setColor(bulbColor1)
                bulb2.setColor(bulbColor2)
                bulb3.setColor(bulbColor3)
            elif(bulbPattern == config.bulbPatternsDict.get('pattern_bulb_wave')):
                print('color wave')
                #todo
                # the bulbs aren't the best at updating quickly, so may be best to keep them static
            else:
                # default to each color picked by web interface
                bulb1.setColor(bulbColor1)
                bulb2.setColor(bulbColor2)
                bulb3.setColor(bulbColor3)
    except(KeyboardInterrupt, SystemExit):
        #print("End of program")
        # disconnect from everything
        bulb1.disconnect()
        bulb2.disconnect()
        bulb3.disconnect()
        serLights.disconnect()
        print("end")
        #turn everything off
