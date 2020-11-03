import RPi.GPIO as GPIO
from time import sleep

enc_pin_1 = 24
enc_pin_2 = 23
enc_button_pin = 17


class Encoder():
    def __init__(self, ep1, ep2, bp):
        self.ep1 = ep1
        self.ep2 = ep2
        self.bp = bp
        self.last_encoded = 0
        self.value = 0
        self.last_value = 0
        self.enc_button_press = False
        self.begin()

    def update_encoder(self, channel):
        e = ((GPIO.input(self.ep1) == GPIO.LOW) << 1) | (GPIO.input(self.ep2) == GPIO.LOW)
        s = (self.last_encoded << 2) | e
        self.value += (s in (13, 4, 2, 11)) - (s in (14, 7, 1, 8))
        self.last_encoded = e

    def enc_button_event(self, channel):
        self.enc_button_press = True

    def begin(self):
        GPIO.setmode(GPIO.BCM)
        for pin in (self.ep1, self.ep2, enc_button_pin):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for pin in (self.ep1, self.ep2):
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.update_encoder, bouncetime=5)
        GPIO.add_event_detect(enc_button_pin, GPIO.FALLING, callback=self.enc_button_event, bouncetime=200)


def main():
    encoder = Encoder(enc_pin_1, enc_pin_2, enc_button_pin)
    while True:
        sleep(.5)
        print(encoder.value, encoder.enc_button_press)
        if encoder.enc_button_press:
            encoder.enc_button_press = False


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\ndone")
    finally:
        GPIO.cleanup() 
