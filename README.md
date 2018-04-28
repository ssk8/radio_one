# radio_one
raspi single button, single station radio
mplayer e.g., http://198.241.60.211:8001/listen.mp3

reconfigure the pins at boot without any external software or services: 
add this line to  /boot/config.txt:

dtoverlay=pwm-2chan,pin=18,func=2,pin2=13,func2=4
