import RPi.GPIO as GPIO
from mplayer import Player
from time import sleep, time
from os import system
from encoder import Encoder

#music = "/home/pi/media/test2.mp3"
#music = "https://5d497a7ce1964.streamlock.net/RK/HD1.stream/playlist.m3u8"
music = "https://radio.stereoscenic.com/asp-s"

enc_pin_1, enc_pin_2 = 24, 23
enc_button_pin, top_button_pin = 17, 27
top_button_press = False


def top_button_event(channel):
    global top_button_press
    top_button_press = True


GPIO.setmode(GPIO.BCM)
GPIO.setup(top_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(top_button_pin, GPIO.FALLING, callback=top_button_event, bouncetime=500)


def get_volume(encoder):
    if encoder.value > 100:
        encoder.value = 100
        return 100
    elif encoder.value < 0:
        encoder.value = 0
        return 0
    else:
        return encoder.value


def playing(player, encoder):
    global top_button_press
    player.loadfile(music)
    player.volume = get_volume(encoder)
    last_encoder_value = encoder.value
    start_time = time()
    while (not top_button_press) and ((time()-start_time)<60*120):
        sleep(.1)
        if encoder.value != last_encoder_value:
            last_encoder_value = encoder.value
            player.volume = get_volume(encoder)
        if encoder.enc_button_press:
            player.pause()
            encoder.enc_button_press = False
    player.stop()
    sleep(1)
    top_button_press = False


def main():
    global top_button_press
    encoder = Encoder(enc_pin_1, enc_pin_2, enc_button_pin)
    encoder.value = 70
    Player.path = "/usr/bin/mplayer"
    player = Player()
    while True:
        sleep(.5)
        if top_button_press: 
            sleep(.5)
            top_button_press, encoder.enc_button_press = False, False
            playing(player, encoder)
            sleep(.5)
        if encoder.enc_button_press:
            sleep(4)
            if top_button_press:
                system('sudo shutdown now -h')
            encoder.enc_button_press = False

            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\ndone")
    finally:
        GPIO.cleanup() 
