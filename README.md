# PatioLightsHost
The host program for the Patio Lights project.

## Background

After doing [Internet-Xmas-Tree](https://github.com/Chris-Johnston/Internet-Xmas-Tree) last year, we wanted to do the same thing for our outdoor Christmas lights.
We figured that this could also be useful for Halloween, 4th of July and whatever arbitrary holidays/events we felt like celebrating.
The plan was to incorporate the same light strips from the tree project, as well as a the wifi enabled lightbulbs I've been playing with.
We mounted several of these light strips to the front of the porch railing, and draped a few on the back side (just for Halloween).
In the light fixtures, we stuck three Wifi enabled RGB Lightbulbs (see [PythonWifiLedBulbController](https://github.com/Chris-Johnston/PythonWifiLedBulbController)).

### Implementation

The whole thing is controlled with an Arduino Mega and a Raspberry Pi.
The Arduino is connected to the PI via serial, and controls each of light strips. 
See [PatioLightsClient](https://github.com/Chris-Johnston/PatioLightsClient) for details.
The Pi runs a web server that hosts the web interface, and runs a script that monitors for any changes in the data entered.
It then controls the lightbulbs and sends data to the Arduino.

## Images of Use

### Halloween Themes

<img src="/resources/halloween1.jpg" width="250" alt="Halloween Lights"/>
<img src="/resources/halloween2.jpg" width="250" alt="Halloween Lights"/>

### Football Themes

<img src="/resources/seahawks1.jpg" width="250" alt="Seahawks Lights"/>
<img src="/resources/huskies1.jpg" width="250" alt="Huskies Lights"/>

todo christmas themes

## Installation and Usage

This project is split up into two components, the host and the client.

This is the page for the host software. The client is located at [PatioLightsClient](https://github.com/Chris-Johnston/PatioLightsClient).

First download and install PHP and Apache2. I'm not going to cover that here.

I recommend downloading each into a parent directory and keeping the host and the client separate.

```bash
# create a parent directory
mkdir Lights
cd Lights
# download each of the repos
git clone https://github.com/Chris-Johnston/PatioLightsHost.git
git clone https://github.com/Chris-Johnston/PatioLightsClient.git
```

Point your Apache configuration at `/somePath/patioLightsHost/www/` for the website source.

The host software contains a configuration file that should be edited (and is platform dependent!). Modify `/patioLightsHost/configuration.ini` to match your needs.
You will have to know what serial port the Arduino running the client software is connected to. Keep the baud rate at 250000, as the client software runs at the same rate.
The configuration file contains the IP address of each of the Wifi enabled bulbs. See [PythonWifiLedBulbController](https://github.com/Chris-Johnston/PythonWifiLedBulbController) for details on getting their IP addresses. *todo implement bulbless mode in configuration.*
Don't modify the pattern values at the bottom of the file.

Often the web data file will have permissions issues when being downloaded. To ensure that PHP can modify the file, run `chmod 777 /patioLightsHost/www/colorData.json`.

The host software contains a script that will have to be run at startup and stay running in the background. I did this by adding it to `/etc/rc.local` before `exit 0`.

```bash
# first delete the log file (if it exists)
rm -f /somePath/PatioLightsHost/patioLightsHost/patioLights.log

# must change directory to patioLightsHost folder before starting program
# & will make the program run in the background
(cd /somePath/PatioLightsHost/patioLightsHost/ && python3 patioLightsHost.py) &
```

For debugging purposes, the script works fine if run manually.

After rebooting, the script should be running in the background. I can verify this by running `ps -aux | grep python3` and seeing my process. If I want to monitor the host script's log, I can view it with the following command:

```bash
# monitor the log file for changes
tail -f /somePath/PatioLightsHost/patioLightsHost/patioLights.log -f
```

Navigate to your webserver and you should see the data entry form. Enter your values, hit submit and ensure that there are no errors in the submit page or the log.

## External Dependencies

HTML Color picker uses [jscolor](http://jscolor.com/).
