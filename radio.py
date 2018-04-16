import subprocess
from time import sleep
import datetime
import RPi.GPIO as GPIO
  
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN)

radio = False

while True:
    if (GPIO.input(19) == False):
        if radio:
            subprocess.call(['killall', 'mplayer'])
            radio = False
            sleep(2)
        else:
            subprocess.Popen(['mplayer', 'http://xxx.xxx.xxx.xxx:8001/listen.mp3'])
            now = datetime.datetime.now() + datetime.timedelta(hours=1)
            radio = True
            sleep(2)
    if radio and datetime.datetime.now() > now:
        subprocess.call(['killall', 'mplayer'])
        radio = False
sleep(0.1);
