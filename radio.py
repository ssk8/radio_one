import RPi.GPIO as GPIO
from mplayer import Player
from time import sleep


enc_pin_1, enc_pin_2 = 23, 24
enc_button_pin, top_button_pin = 17, 27
last_encoded, encoder_value, last_encoder_value = 0, 70, 0
enc_button_press, top_button_press = False, False


def update_encoder(channel=0):
    global encoder_value
    global last_encoded
    MSB = GPIO.input(enc_pin_1) == GPIO.LOW
    LSB = GPIO.input(enc_pin_2) == GPIO.LOW
    encoded = (MSB << 1) | LSB
    summed  = (last_encoded << 2) | encoded
    if summed in (13, 4, 2, 11): encoder_value +=1
    if summed in (14, 7, 1, 8): encoder_value -=1
    last_encoded = encoded


def enc_button_press_event(channel=0):
    global enc_button_press
    enc_button_press = True


def top_button_press_event(channel=0):
    global top_button_press
    top_button_press = True


GPIO.setmode(GPIO.BCM)
for pin in (enc_pin_1, enc_pin_2, enc_button_pin, top_button_pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in (enc_pin_1, enc_pin_2):
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=update_encoder)
GPIO.add_event_detect(enc_button_pin, GPIO.FALLING, callback=enc_button_press_event)
GPIO.add_event_detect(top_button_pin, GPIO.FALLING, callback=top_button_press_event)


def get_volume():
    if encoder_value>100:
         return 100
    elif encoder_value<0:
        return 0
    else:
        return encoder_value

def playing(player):
    global enc_button_press, top_button_press
    #player.loadfile("test2.mp3")
    
    player.loadfile("https://radio.stereoscenic.com/asp-s")
    while not top_button_press:
        sleep(.5)
        if encoder_value != last_encoder_value:
            player.volume = get_volume()
        if enc_button_press:
            player.pause()
            enc_button_press = False
    top_button_press =  False
    player.stop()
    sleep(1)


def main():
    global enc_button_press, top_button_press
    Player.path = "/usr/bin/mplayer"
    player = Player()
    while True:
        sleep(.5)
        if top_button_press:
            top_button_press, enc_button_press =  False, False
            playing(player)


if __name__ == "__main__":
    main()
