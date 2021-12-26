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
apt install python3-pip git vim mplayer
python3 -m pip install mplayer.py
