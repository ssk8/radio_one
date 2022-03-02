# radio_one
raspberry pi based "single button" radio (I guess there are technically 2 buttons now)

### Concept: stream one station, one button to start/stop

2022 change:
- add audio navigation hints
- ability to change stations (when the "one" is down)

2020 change: 
- I2S DAC/amp 
- rotary encoder for volume. encoder button pauses and shuts down if top button is held

<img src=https://github.com/ssk8/project_pics/blob/main/radio_out.jpg width="300"/>

<img src=https://github.com/ssk8/project_pics/blob/main/radio_guts.jpg width="300"/>


for setup:
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh

follow: https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/pi-i2s-tweaks

apt install python3-pip git vim mpv

python3 -m pip install pyalsaaudio python-mpv

crontab -e >> @reboot sleep 20 && python3 /home/pi/radio_one/radio.py
