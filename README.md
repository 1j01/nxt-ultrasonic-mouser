
# NXT Ultrasonic Mouser

Using the Lego Mindstorms NXT 2.0 Ultrasonic Sensor to play [Plink](http://labs.dinahmoe.com/plink/) like a [theremin](https://en.wikipedia.org/wiki/Theremin) and games like a boss.

## Setup

Using Python 2.7, PyMouse, nxt-python-2.2.2

Let me be frank, this thing is probably a pain to set up. Maybe not on linux, though?

### Linux

Instructions are for USB connection, but [nxt-python](https://code.google.com/p/nxt-python/wiki/Installation) also allows for Bluetooth and NXT's Fantom driver.

```shell
cd nxt-python
sudo python setup.py install
cd ../PyMouse
sudo python setup.py install
cd ..
sudo apt-get install python-xlib python-usb
```

That should work, more or less. I haven't exactly tested it, as such.

### Windows

You'll need to open up an administrative command prompt and get your hands dirty.

##### PyMouse

PyMouse depends on [pywin32](http://sourceforge.net/projects/pywin32/files/) and [pyHook](http://sourceforge.net/projects/pyhook/files/pyhook/).
You can download installers for those from their project pages on SourceForge.
Run `python` (`^Z Enter`) to see whether you have 64bit or 32bit python installed.
Download the appropriate installers based on this.

##### NXT-Python

For nxt-python to work, you need to install a communication module.

###### PyBluez

Bluetooth is probably the easiest method.
Obviously it requires either a Bluetooth dongle or built-in Bluetooth functionality.

Install PyBluez with `pip install pybluez` or by downloading and running their installer on PyPI.

###### PyFantom

I got this to work for about ten seconds after searching for, downloading, extracting and installing
Lego's [NXT Fantom Driver](http://www.lego.com/en-us/mindstorms/downloads/nxt/nxt-fantom-driver/),
searching for, downloading, extracting and installing PyFantom
which says windows support is "to be determined"
and then gives an error "Unsupported platform",
rage-quiting,
suspecting it's an outdated version,
finding, downloading, extracting and installing the master version
and updating all my code.

Then it stopped working.

###### PyUSB

NXT-Python has it's backends and one of them is PyUSB. PyUSB has its own set of backends.

Some of them seem to support Windows.

...and libusb-win32 just sort of blocked even the official NXT software from connecting to the NXT and it's all like
"The device driver can not be easily removed from the system.
You can however try to use [​usbdeview](#IamNotInstallingSomethingToUninstallSomething!)
to remove the entries..."
You can however uninstall it from the "Device Manager" (without downloading additional software!)

### Mac

I don't have a mac.

## Usage

It's not supposed to move the mouse when you're not interacting with it, but if it goes rouge, just turn off your NXT.

1. Turn on the NXT and connect it to your computer.
2. Connect the Ultrasonic sensor to port 4. You'll probably want to attach it directly to the NXT brick.
3. Use `sudo python main.py`. (If you don't want to use sudo, you can apparently configure some udev rules for USB access, but I haven't tried this)
4. You'll probably get a BrickNotFound error or something else. Good luck.
5. Calibration: Follow the instructions. If you want to use it by casually pointing, calibrate it by casually pointing. The settings are stored in `config.ini`. To recalibrate, use `sudo python main.py --recalibrate`

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

	* Separate calibration configurations


* Configure on-screen boundaries
	
	* Listen to mouse events to let the user draw a line to define the boundaries
	
	* Add to configuration (config.ini)


* Smoothing
