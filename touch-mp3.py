import MPR121
from gpiozero import RGBLED
import subprocess
import pygame
from pygame.mixer import Sound
from glob import glob
from time import sleep
from flask import Flask
from flask import render_template
import threader
import threading

class AThread(threading.Thread):
    def run(self):
        from time import sleep
        while True:
            print "I'm running...and I'll never end!"
            sleep(5)

    def end(self):
        if self.is_alive():
            threader.killThread(str(integer).decode(self.ident))

runMe = AThread()
runMe.start()
sleep(10)
runMe.end()

class AFlaskThread(threading.Thread):
    def run(self):
        app = Flask(__name__)

        @app.route('/json')
        def json():
            return render_template('json.html')

        @app.route('/sounds')
        def sounds():
            soundsStart()
            return "nothing"

        @app.route('/birthday')
        def birthday():
            soundsEnd()
            return "nothing"

        app.run(host='0.0.0.0', port= 80)

    def end(self):
        if self.is_alive():
            threader.killThread(self.ident)

class ASoundsThread(threading.Thread):
    def run(self):
        sensor = MPR121.begin()
        sensor.set_touch_threshold(40)
        sensor.set_release_threshold(20)

        led = RGBLED(6, 5, 26, active_high=False)

        num_electrodes = 12

        # convert mp3s to wavs with picap-samples-to-wav
        led.blue = 1
        subprocess.call("picap-samples-to-wav tracks", shell=True)
        led.off()

        # initialize mixer and pygame
        pygame.mixer.pre_init(frequency=44100, channels=64, buffer=1024)
        pygame.init()

        sounds = [Sound(path) for path in glob("tracks/.wavs/*.wav")]

        def play_sounds_when_touched():
            if sensor.touch_status_changed():
                sensor.update_touch_data()

                is_any_touch_registered = False

                for i in range(num_electrodes):
                    if sensor.get_touch_data(i):
                        # check if touch is registered to set the led status
                        is_any_touch_registered = True
                    if sensor.is_new_touch(i):
                        # play sound associated with that touch
                        print ("playing sound: " + str(i))
                        sound = sounds[i]
                        sound.play()

                if is_any_touch_registered:
                    led.red = 1
                else:
                    led.off()

        running = True
        while running:
            try:
                play_sounds_when_touched()
            except KeyboardInterrupt:
                led.off()
                running = False
            sleep(0.01)

    def end(self):
        print ("self = " + self)
        print ("self.ident = " + self.ident)
        if self.is_alive():
            threader.killThread(self.ident)


if __name__ == '__main__':
    sounds = ASoundsThread()

    def soundsStart():
        sounds.start()

    def soundsEnd():
        sounds.end()

    flask = AFlaskThread()
    flask.start()
