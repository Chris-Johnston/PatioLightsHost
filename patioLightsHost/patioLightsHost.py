from GlobalConfiguration import GlobalConfiguration
import serial
import time
import random
from WifiBulb import WifiBulb
from SerialLightController import SerialLightController

ser = serial.Serial()

# patio lights main script
config = GlobalConfiguration("configuration.ini")

if __name__ == "__main__":
    print("Start of program")
    config = GlobalConfiguration("configuration.ini")
    config.load()
    
    # configuration loaded
    # open serial connection
    #try:
    #    ser = serial.Serial(config.SerialPort, config.BaudRate, timeout = 1)
    #except Exception:
    #    print("Error opening serial connection! (Check configuration.ini)")
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
        #bulb1.connect()
        bulb2.connect()
        #bulb3.connect()
    except Exception as e:
        print("Failed to connect to one or more lightbulbs! " + str(e))

    try:
        while(True):
            # read the contents of the file again
            try:
                file = open(config.DataFile, "rb")
            except FileNotFoundError:
                print("Web data file not found!")
            # placeholder operation, just pulses the first bulb on and off
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            #cmdStr = getSerialCommand('0', color, (0, 0, 0), 40, 0)
            #cmdBytes = bytes(cmdStr, 'utf-8')
            serLights.setPatternAndColors('4', color, (0,0,0), 400, 0)
            #if (ser.isOpen() == False):
            #    ser.open()
            #ser.write(cmdBytes)
            #ser.flush()
            #ser.close()
            #bulb1.setColor(color)
            bulb2.setColor(color)
            #bulb3.setColor(color)
            time.sleep(1)
            #cmdStr = getSerialCommand('0', (0,0,0), (0, 0, 0), 40, 0)
            #cmdBytes = bytes(cmdStr, 'utf-8')
            #ser.open()
            #ser.write(cmdBytes)
            #ser.flush()
            #ser.close()
            #bulb1.setColor((0,0,0))
            #bulb2.setColor((0,0,0))
            #serLights.setPatternAndColors('0', (0,0,0), (0,0,0), 40, 0)
            #bulb3.setColor((0,0,0))
            #time.sleep(0.5)
    except(KeyboardInterrupt, SystemExit):
        print("End of program")
        # turn off the bulbs
        #bulb1.setColor((0,0,0))
        #bulb1.disconnect()
        bulb2.disconnect()
        #bulb3.setColor((0,0,0))
        #bulb3.disconnect()
        serLights.disconnect()
        print("end")
        #turn everything off
