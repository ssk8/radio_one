import RPi.GPIO as GPIO
import mpv
import alsaaudio
from time import sleep, time
from os import system
from encoder import Encoder
import json
from pathlib import Path
from dataclasses import dataclass


radio_data_path = Path(__file__).parent.parent / "media"
radio_data_file = radio_data_path / "radio_data.json"
radio_nav_path = radio_data_path / "navigation"

enc_pin_1, enc_pin_2 = 24, 23
enc_button_pin, top_button_pin = 17, 27
last_encoder = 0
top_button_press = False

def top_button_event(channel):
    global top_button_press
    top_button_press = True


@dataclass
class Media:
    id: str
    nav_path: Path
    media_path: str = None
    station: bool = False


class MediaLibrary:
    _media = dict()
    _player = mpv.MPV()
    _current_station = 0

    def __init__(self, media_data_file: Path) -> None:
        with open(media_data_file) as f:
            self._media_data = json.load(f)
        for file in self._media_data:
            id = file.get("id")
            nav_path = Path(file.get("nav_file"))
            media_path = file.get("media_path")
            station = bool(file.get("station"))
            self._media[id] = Media(
                id=id, nav_path=nav_path, media_path=media_path, station=station
            )
        self._stations = [m for m in self._media.values() if m.station]

    def play(self, media_to_play):
        self._player.play(str(media_to_play))

    def play_nav(self, nav):
        self.play(radio_nav_path / nav.nav_path)

    def startup_nav(self):
        self.play_nav(self._media["startup"])

    def shutdown_instruct_nav(self):
        self.play_nav(self._media["shutdown_instruction"])
    
    def shutdown_nav(self):
        self.play_nav(self._media["shutdown"])
        sleep(2)

    def next_station(self, up: bool):
        self._current_station = (self._current_station + (up or -1))%len(self._stations)
        self.play_nav(self._stations[self._current_station])

    def play_station(self):
        self.play(self._stations[self._current_station].media_path)

    def stop(self):
        self._player.stop()


def adjuist_volume(alsa_mixer, up: bool):
    min_volume, max_volume, increment = 5, 90, 5
    current = alsa_mixer.getvolume()[0]
    if up:
        alsa_mixer.setvolume(min(max_volume, current+increment))
    else:
        alsa_mixer.setvolume(max(min_volume, current-increment))


def standby_mode(media, alsa_mixer, encoder):
    global top_button_press, last_encoder
    last_encoder_value = encoder.value
    while not top_button_press:
        if abs((cv:=encoder.value) - last_encoder_value)>5:
            media.next_station(bool(cv>last_encoder_value))
            last_encoder_value = encoder.value
        if encoder.enc_button_press:
            media.shutdown_instruct_nav()
            sleep(4)
            if top_button_press:
                media.shutdown_nav()
                system('sudo shutdown now -h')
            encoder.enc_button_press = False
        sleep(.5)
    top_button_press, encoder.enc_button_press = False, False
    playing_mode(media, alsa_mixer, encoder)


def playing_mode(media, alsa_mixer, encoder):
    global top_button_press, last_encoder
    started_playing_time = time()
    last_encoder_value = encoder.value
    media.play_station()
    while (not top_button_press) and ((time()-started_playing_time)<60*120):
        if (cv:=encoder.value) != last_encoder_value:
            adjuist_volume(alsa_mixer, bool(cv>last_encoder_value))
            last_encoder_value = encoder.value
        sleep(.5)
    media.stop()
    top_button_press, encoder.enc_button_press = False, False
    standby_mode(media, alsa_mixer, encoder)


def main():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(top_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(top_button_pin, GPIO.FALLING, callback=top_button_event, bouncetime=500)
    media = MediaLibrary(radio_data_file)
    encoder = Encoder(enc_pin_1, enc_pin_2, enc_button_pin)
    alsa_mixer = alsaaudio.Mixer('PCM')
    alsa_mixer.setvolume(70)
    media.startup_nav()
    standby_mode(media, alsa_mixer, encoder)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\ndone")
    finally:
        GPIO.cleanup() 
