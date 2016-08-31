
This is a baby monitor project using a raspberry pi, picamera
and usb camera to monitor baby roon's image and sound.

The app will run on local host on port 5000 (0.0.0.0:5000)

The software is written in python2.7 and the web interface uses flask, with some
bootstrap for the visual. 
The interface has an open welcome page and a logign required camera, audio, setup
and configuration pages.

The camera used is NoIR and IR Leds are automatic turned on when the light is low.*

On the settings, there will be options for motion capture and warnning when a 
threshold is reached*.

*Features not yet implemented:
	- Audio streamming
	- IR Led
	- Motion detection
	- Light threshold


This is a home project and most of web interface, I used Miguel Grinberg's 
Book "Flask web development" and his github project 
["flask-video-streaming"](https://github.com/miguelgrinberg/flask-video-streaming)
