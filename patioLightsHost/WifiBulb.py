import socket
import binascii
from threading import Thread

def getChecksumValue(byteArray):
        """ returns the checksum value as a byte from an array of bytes """
        #sum all the values
        sumOfValues = 0
        for x in range(len(byteArray)):
            sumOfValues += byteArray[x]
        # return 
        return sumOfValues % pow(2, len(byteArray) + 1)

class WifiBulb(object):
    """class for controlling a wifi lightbulb"""
    mode = "31" # default mode
    magicBytes = "00f00f" # have yet to investigate what these do
    PORT = 5577
    #s = socket.socket()

    def __init__(self, IP):
        """ constructor with IP address """
        self.IP = IP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _connect(self):
        """ thread for connecting to the bulb """
        print ("Connecting to : " + self.IP + " : " + str(WifiBulb.PORT) )
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.IP, WifiBulb.PORT))
            print ("Connected to " + self.IP + ":" + str(WifiBulb.PORT))
        except:
            raise Exception("Failed to connect to lightbulb! IP: " + str(self.IP))
            print ("failed to connect")

    def connect(self):
        """ connects the socket """
        self.connectionThread = Thread(target=self._connect)
        self.connectionThread.start()

    def disconnect(self):
        """ disconnects the socket """
        self._setColor((0,0,0))
        self.s.detach()

    def _setColor(self, color):
        """thread for setting the color """
        print("Sending color: " + str(color))
        # mode + red + green + blue + magicBytes + checksum
        message = WifiBulb.mode + format(color[0], "02x") + format(color[1], "02x") + format(color[2], "02x") + WifiBulb.magicBytes 
        messageBytes = bytearray.fromhex(message)
        checksum = getChecksumValue(messageBytes)
        messageBytes.append(checksum)
        try:
            self.s.send(messageBytes)
        except:
            print("Failed to set color")

    def setColor(self, color):
        """sets the color the given tuple in the format (R, G, B)"""
        self.setColorThread = Thread(target=self._setColor, args=(color,))
        self.setColorThread.start()