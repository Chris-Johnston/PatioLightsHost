# Patio Lights Controller
import configparser

# class to store configuration values
class GlobalConfiguration(object):
    SerialPort = "none"
    BaudRate = 115200
    DataFile = "nofile"
    Lightbulb1_IP = "noIP"
    Lightbulb2_IP = "noIP"
    Lightbulb3_IP = "noIP"
    patternsDict = {}

    def __init__(self, path):
        """ constructor """
        self.SerialPort = "none"
        self.BaudRate = 115200
        self.DataFile = path
        self.Lightbulb1_IP = "noIP"
        self.Lightbulb2_IP = "noIP"
        self.Lightbulb3_IP = "noIP"
        self.patternsDict = {}

    def load(self):
        """ loads the data from the configuration file """
        # load data from the configuration
        Config = configparser.ConfigParser()
        Config.read("configuration.ini")

        # Configuration data
        try:
            # Serial communication data for the arduino
            self.SerialPort = Config.get("Configuration", "SerialPort")
            self.BaudRate = Config.get("Configuration", "BaudRate")
            # load the path to the color data file from configuration
            self.DataFile = Config.get("Configuration", "DataFile")
            # load the lightbulb ip addresses
            self.Lightbulb1_IP = Config.get("Configuration", "Lightbulb1IP")
            self.Lightbulb2_IP = Config.get("Configuration", "Lightbulb2IP")
            self.Lightbulb3_IP = Config.get("Configuration", "Lightbulb3IP")
            self.patternsDict = dict(Config.items("Patterns"))

        except Exception as e:
            print("Error fetching configuration data from file.")
            raise Exception("Error fetching configuration data" + str(e))
