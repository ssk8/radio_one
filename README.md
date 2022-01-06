# radio_one
raspberry pi based "single button" radio (I guess there are technically 2 buttons now)

### Concept: stream one station, one button to start/stop

2020 upgrade: 
- I2S DAC/amp 
- rotary encoder for volume. encoder button pauses and shuts down if top button is held

![](https://raw.githubusercontent.com/ssk8/radio_one/master/radio_out.jpg)

![](https://raw.githubusercontent.com/ssk8/radio_one/master/radio_guts.jpg)


for setup:
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh

follow: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pi-i2s-tweaks

apt install python3-pip git vim mpv

python3 -m pip install pyalsaaudio python-mpv

crontab -e >> @reboot sleep 20 && python3 /home/pi/radio_one/radio.py
