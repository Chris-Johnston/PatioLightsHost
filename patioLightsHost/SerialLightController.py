from GlobalConfiguration import GlobalConfiguration
import serial
import json
from threading import Thread

class SerialLightController(object):
    ser = serial.Serial()

    def getSerialString(self, patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed, width):
        str = ""
        str = str + self.config.patternsDict.get('start_of_message')
        #str += "1" # just do the front lights for now
        str += patternValue
        str += '{:03d}'.format(color1tuple[0]) # color 1 r g b
        str += '{:03d}'.format(color1tuple[1])
        str += '{:03d}'.format(color1tuple[2])
        str += '{:03d}'.format(color2tuple[0]) # color 2 r g b
        str += '{:03d}'.format(color2tuple[1])
        str += '{:03d}'.format(color2tuple[2])
        str += '{:04d}'.format(animationSpeed)
        str += '{:04d}'.format(holdSpeed)
        str += '{:03d}'.format(width)
        str += self.config.patternsDict.get('end_of_message')
        str += '\n'
        return str

    def __init__(self, globalConfig):
        """ constructor """
        self.config = globalConfig

    def _connect(self):
        try:
            self.ser = serial.Serial(self.config.SerialPort, self.config.BaudRate, timeout = 1)
            print("connected to serial")
        except Exception as e:
            print(e)
            print("Error opening serial connection!")

    def connect(self):
        self.connectionThread = Thread(target=self._connect)
        self.connectionThread.start()

    def disconnect(self):
        """ disconnects """
        # ensure that it turns off before closing
        #self._setPatternAndColors('0', (0,0,0), (0,0,0), 0, 0)
        self.ser.flush()
        self.ser.close()

    def sendMessage(self, message):
        """ send message over serial"""
        # only if open
        if(self.ser.isOpen()):
            try:
                cmdBytes = bytes(message, 'utf-8')
                print("\nWriting", cmdBytes)
                self.ser.write(cmdBytes)
                self.ser.flush()
            except Exception as e:
                print(e)
                print("error sending message : " + message)

    def _setPatternAndColors(self, patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed, width):
        try:
            command = self.getSerialString(patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed, width)
            self.sendMessage(command)
        except Exception as e:
            print(e)
            print("Error setting pattern and colors")

    def setPatternAndColors(self, patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed, width):
        print("setting pattern")
        self.writeThread = Thread(target=self._setPatternAndColors, args=(patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed,width))
        self.writeThread.start()