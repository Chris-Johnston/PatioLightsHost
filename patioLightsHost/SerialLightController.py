from GlobalConfiguration import GlobalConfiguration
import serial
import json
import time
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
        # checksum value
        # add up values and % 99
        # checksum value 99 is always accepted
        str += '{:02d}'.format((color1tuple[0] + color1tuple[1] + color1tuple[2] + color2tuple[0] + color2tuple[1] + color2tuple[2] + animationSpeed + holdSpeed + width) % 99)
        str += self.config.patternsDict.get('end_of_message')
        str += '\n'
        return str

    def __init__(self, globalConfig):
        """ constructor """
        self.config = globalConfig

    def _connect(self):
        try:
            self.ser = serial.Serial(self.config.SerialPort, self.config.BaudRate)
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
                #message = 's72550000000000000001500225008e\r'
                cmdBytes = bytes(message, 'utf-8')
                # print the garbage character
                print("x")
                #self.ser.write(bytes('\r' + 'x'*100 + '\r', 'utf-8'))
                self.ser.write(b'x')
                
                #self.ser.flush()
                #self.ser.flushOutput()
                #time.sleep(0.1)
                time.sleep(0.05)
                #print(self.ser.readline())
                # wait for response

                #while ("Useless" not in response):
                    #print(bytes('x'*100, 'utf-8'))
                #    self.ser.write(bytes('x'*100, 'utf-8'))
                #    #self.ser.flushOutput()
                #    time.sleep(0.1)
                #    response = str(self.ser.read_all())
                #    print(response)
                print("\nWriting", cmdBytes)
                # then print the actual data
                #self.ser.write(cmdBytes)
                self.ser.write(cmdBytes)
                self.ser.flushOutput()
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