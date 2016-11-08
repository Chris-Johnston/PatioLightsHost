from GlobalConfiguration import GlobalConfiguration
import serial
import json
from threading import Thread

class SerialLightController(object):
    ser = serial.Serial()

    def getSerialStringOld(self, patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed):
        str = ""
        str += self.config.patternsDict.get('start_of_message')
        str += "1" # just do the front lights for now
        str += patternValue
        str += '{:03d}'.format(color1tuple[0]) # color 1 r g b
        str += '{:03d}'.format(color1tuple[1])
        str += '{:03d}'.format(color1tuple[2])
        str += '{:03d}'.format(color2tuple[0]) # color 2 r g b
        str += '{:03d}'.format(color2tuple[1])
        str += '{:03d}'.format(color2tuple[2])
        str += '{:04d}'.format(animationSpeed)
        str += '{:04d}'.format(holdSpeed)
        str += self.config.patternsDict.get('end_of_message')
        str += '\n'
        return str

    # using JSON instead of binary data to make things more readable
    def getJSONStr(self, pattern, color1, color2, animationSpeed, holdSpeed):
        data = {}
        data["pattern"] = pattern
        data["color1"] = color1
        data["color2"] = color2
        data["animationSpeed"] = animationSpeed
        data["holdSpeed"] = holdSpeed
        str = json.dumps(data, indent = 4)
        #debug
        print(str)
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
        self._setPatternAndColors('0', (0,0,0), (0,0,0), 0, 0)
        self.ser.flush()
        self.ser.close()

    def _setPatternAndColors(self, patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed):
        try:
            print("pattern")
            command = self.getSerialStringOld(patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed)
            cmdBytes = bytes(command, 'utf-8')
            self.ser.write(cmdBytes)
        except Exception as e:
            print(e)
            print("Error setting pattern and colors")

    def setPatternAndColors(self, patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed):
        print("setting pattern")
        self.writeThread = Thread(target=self._setPatternAndColors, args=(patternValue, color1tuple, color2tuple, animationSpeed, holdSpeed))
        self.writeThread.start()