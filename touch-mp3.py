import MPR121
from gpiozero import RGBLED
import subprocess
import pygame
from pygame.mixer import Sound
from glob import glob
from time import sleep
from flask import Flask
from flask import render_template
from threading import Thread

mode = "sounds"

def flaskThread():

    app = Flask(__name__)

    @app.route('/json')
    def json():
        return render_template('json.html')

    @app.route('/sounds')
    def sounds():
        global mode
        mode= "sounds"
        return "nothing"

    @app.route('/birthday')
    def birthday():
        global mode
        mode = "birthday"
        return "nothing"

    app.run(host='0.0.0.0', port= 80)

def touchThread():
    sensor = MPR121.begin()
    sensor.set_touch_threshold(40)
    sensor.set_release_threshold(20)

    led = RGBLED(6, 5, 26, active_high=False)

    num_electrodes = 12

    # convert mp3s to wavs with picap-samples-to-wav
    led.blue = 1
    subprocess.call("picap-samples-to-wav tracks", shell=True)
    subprocess.call("picap-samples-to-wav birthday-tracks", shell=True)
    led.off()

    # initialize mixer and pygame
    pygame.mixer.pre_init(frequency=44100, channels=64, buffer=1024)
    pygame.init()


    def play_sounds_when_touched():
        sounds = [Sound(path) for path in glob("tracks/.wavs/*.wav")]
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

    def play_birthday_when_touched():
        sounds = [Sound(path) for path in glob("birthday-tracks/.wavs/*.wav")]
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
            global mode
            if mode == "sounds":
                play_sounds_when_touched()
            elif mode == "birthday":
                play_birthday_when_touched()
            else:
                print("no mode set")

        except KeyboardInterrupt:
            led.off()
            running = False
        sleep(0.01)

if __name__ == '__main__':
    Thread(target = touchThread).start()
    Thread(target = flaskThread).start()
