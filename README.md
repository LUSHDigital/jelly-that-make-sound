# jelly-that-make-sound

## Prerequisites

A [Bare Conductive Pi Cap](https://www.bareconductive.com/shop/pi-cap) + [Raspberry Pi](https://shop.pimoroni.com/products/raspberry-pi-3-b-plus) & it's [Power Supply](https://shop.pimoroni.com/products/raspberry-pi-universal-power-supply).

![Pi-Cap](https://www.bareconductive.com/wp-content/uploads/2010/07/IMG_1048_PiCap_RaspPi-1-720x415.png)

## Setup

Flash the Pi's SD with [Raspbian](https://www.raspberrypi.org/downloads/raspbian), then boot and SSH to the Pi.

1. Install picap package.

`sudo apt-get install picap`

2. Run picap setup.

`picap-setup` - Bare Conductive strongly recommend you enable high quality audio.

3. Pull this repo.

`git clone https://github.com/LUSHDigital/jelly-that-make-sound.git`

## Run on boot

To set the script to run on boot edit rc.local:

`sudo nano /etc/rc.local`

Assuming you pulled the repo to home, add the following line above `exit 0`:

`cd /home/pi/jelly-that-make-sound/ && sudo python3 touch-mp3.py &`
