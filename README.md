
# NXT Ultrasonic Mouser

Using the Lego Mindstorms NXT 2.0 Ultrasonic Sensor to play [Plink](http://labs.dinahmoe.com/plink/) like a [theremin](https://en.wikipedia.org/wiki/Theremin) and games like a boss.

## Setup

The libraries this uses are supposed to be cross-platform, but I haven't gotten it to work on Windows yet.

Let me be frank, this thing is probably a pain to set up. Maybe it's not, though...

I'm using Python 2.7.6

### Linux

```shell
cd nxt-python-0.7
sudo python setup.py install
cd ../PyMouse
sudo python setup.py install
cd ..
sudo apt-get install python-xlib python-usb
```

### Windows

Hmm, maybe I needed to install things from an administrative command prompt...
Ugh, but the USB situation. It seems like you have to install libusb-win32 (none of the other ones seem to have windows support)...
and libusb-win32 just sort of blocked even the official NXT software from connecting to the NXT and it's all like
"The device driver can not be easily removed from the system. You can however try to use ​usbdeview to remove the entries..."
Wow. You can however uninstall it without downloading anything else by going into the Device Manager

## Usage

It's not supposed to move the mouse when you're not interacting with it, but if it goes rouge, just turn off your NXT.

1. Turn on the NXT and connect it to your computer. Duh.
1. Use `sudo python main.py`. (Without sudo I get `usb.USBError: could not set config 1: Operation not permitted`)
1. You'll probably get a BrickNotFound error or something else. The BrickNotFound error can also mean some things aren't installed. Good luck.
1. Connect the Ultrasonic sensor to port 4. (You'll probably want to attach it directly to the NXT brick)
1. Calibration: Follow the instructions. If you want to use it sitting down, calibrate it by casually pointing to the top and bottom of the screen. To recalibrate, use `sudo python main.py recalibrate`

```
usage: main.py [-h] [-r] [-x] [-c] [-b]

NXT Ultrasonic Mouser

optional arguments:
  -h, --help         show this help message and exit
  -r, --recalibrate  Recalibrate the sensor to the screen
  -x, --horizontal   Use horizontal mode (point sensor across screen to the right)
  -c, --clicky       Auto-click repeatedly while interacting
  -b, --bounds       Choose the on-screen bounds for auto-clicking

```

# Todo

* Horizontal mode

* Recover from the occasional `nxt.error.DirProtError: Communication bus error`

* Bluetooth instructions?

