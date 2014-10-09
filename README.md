
# NXT Ultrasonic Mouser

Using the Lego Mindstorms NXT 2.0 Ultrasonic Sensor to play [Plink](http://labs.dinahmoe.com/plink/) like a [theremin](https://en.wikipedia.org/wiki/Theremin) and games like a boss.

## Setup

Using Python 2.7.6

Let me be frank, this thing is probably a pain to set up. Maybe it's not, though?

Instructions are for USB connection, but [nxt-python](https://code.google.com/p/nxt-python/wiki/Installation) also allows for Bluetooth and some kind of apparition.

### Linux

```shell
cd nxt-python-0.7
sudo python setup.py install
cd ../PyMouse
sudo python setup.py install
cd ..
sudo apt-get install python-xlib python-usb
```

That should work, more or less. I haven't exactly tested it, as such.

### Windows

The libraries this uses are supposed to be cross-platform, but I haven't gotten it to work on Windows yet.

Hmm, maybe I needed to install things from an administrative command prompt...
Ugh, but the USB situation. It seems like you have to install libusb-win32 (none of the other ones seem to have windows support)...
and libusb-win32 just sort of blocked even the official NXT software from connecting to the NXT and it's all like
"The device driver can not be easily removed from the system. You can however try to use [​usbdeview](#IamNotInstallingSomethingToUninstallSomething!) to remove the entries..."
You can however uninstall it from the "Device Manager" (without downloading additional software!)

### Mac

I don't have a mac.

## Usage

It's not supposed to move the mouse when you're not interacting with it, but if it goes rouge, just turn off your NXT.

1. Turn on the NXT and connect it to your computer. Duh.
1. Use `sudo python main.py`. (Without sudo I get `usb.USBError: could not set config 1: Operation not permitted`)
1. You'll probably get a BrickNotFound error or something else. The BrickNotFound error can also mean some things aren't installed. Good luck.
1. Connect the Ultrasonic sensor to port 4. (You'll probably want to attach it directly to the NXT brick)
1. Calibration: Follow the instructions. If you want to use it sitting down, calibrate it by casually pointing to the top and bottom of the screen. To recalibrate, use `sudo python main.py --recalibrate`

```
usage: (sudo) main.py [-h] [-d {left,right,up,down}] [-r] [-c] [-b] [-w]

NXT Ultrasonic Mouser

optional arguments:
  -h, --help            show this help message and exit
  -d {left,right,up,down}, --direction {left,right,up,down}
                        the direction the sensor is pointing across the screen (default: up)
  -r, --recalibrate     recalibrate the sensor to the screen
  -c, --clicky          auto-click repeatedly while interacting
  -b, --bounds          choose the on-screen bounds for auto-clicking

```

# Todo

* Fully support horizontal mode

	* Seperate calibration configurations


* Configure on-screen boundaries
	
	* Listen to mouse events to let the user draw a line to define the boundaries
	
	* Add to configuration (config.ini)


* Smoothing

