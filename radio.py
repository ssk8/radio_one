import RPi.GPIO as GPIO
from mplayer import Player
from time import sleep
from os import system

music = "/home/pi/media/test2.mp3"
#music = "https://radio.stereoscenic.com/asp-s"

enc_pin_1, enc_pin_2 = 24, 23
enc_button_pin, top_button_pin = 17, 27
last_encoded, encoder_value, last_encoder_value = 0, 70, 0
enc_button_press, top_button_press = False, False


def update_encoder(channel):
    global encoder_value, last_encoded
    encoded = ((GPIO.input(enc_pin_1) == GPIO.LOW) << 1) | (GPIO.input(enc_pin_2) == GPIO.LOW)
    s = (last_encoded << 2) | encoded
    encoder_value += (s in (13, 4, 2, 11)) - (s in (14, 7, 1, 8))
    last_encoded = encoded


def enc_button_event(channel):
    global enc_button_press
    if GPIO.input(top_button_pin) == GPIO.LOW:
        print("\nshutdown")
        system('sudo shutdown now -h')
    enc_button_press = True


def top_button_event(channel):
    global top_button_press
    top_button_press = True


GPIO.setmode(GPIO.BCM)
for pin in (enc_pin_1, enc_pin_2, enc_button_pin, top_button_pin):
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in (enc_pin_1, enc_pin_2):
    GPIO.add_event_detect(pin, GPIO.FALLING, callback=update_encoder, bouncetime=5)
GPIO.add_event_detect(enc_button_pin, GPIO.FALLING, callback=enc_button_event, bouncetime=500)
GPIO.add_event_detect(top_button_pin, GPIO.FALLING, callback=top_button_event, bouncetime=500)


def get_volume():
    if encoder_value > 100:
        return 100
    elif encoder_value < 0:
        return 0
    else:
        return encoder_value


def playing(player):
    global enc_button_press, top_button_press, last_encoder_value
    player.loadfile(music)
    while not top_button_press:
        sleep(.5)
        if encoder_value != last_encoder_value:
            last_encoder_value = encoder_value
            player.volume = get_volume()
        if enc_button_press:
            player.pause()
            enc_button_press = False
    player.stop()
    sleep(1)
    top_button_press = False


def main():
    global enc_button_press, top_button_press
    Player.path = "/usr/bin/mplayer"
    player = Player()
    while True:
        sleep(.5)
        if top_button_press:
            sleep(.5)
            top_button_press, enc_button_press = False, False
            playing(player)
            sleep(.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\ndone")
    finally:
        GPIO.cleanup() 
