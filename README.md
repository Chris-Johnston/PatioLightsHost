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

### Christmas Themes

todo get xmas pictures
