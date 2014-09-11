
# NXT Plink Theramin

Using the Lego Mindstorms NXT 2.0 Ultrasonic Sensor to play [Plink](http://labs.dinahmoe.com/plink/) like a [theramin](https://en.wikipedia.org/wiki/Theremin) and games like a boss.

# Setup

The things this uses are supposed to be cross-platform, but I haven't gotten it to work on Windows yet.

Let me be frank, this thing is probably a pain to set up. There's like a bunch of libraries and you might even have to install some of their dependencies, I don't remember...

You need to run `sudo python setup.py install` in some directories (ntx-python & pymouse),
and/or some things you can install like `sudo apt-get install python-usb`

`sudo apt-get install python-xlib`

Hmm, maybe I needed to install things from an admin cmd prompt... Ugh, but the USB situation. It seems like you have to install libusb-win32 (none of the other ones seem to have windows support)... and libusb-win32 is all like "The device driver can not be easily removed from the system. You can however try to use ​usbdeview to remove the entries..." Wow. You can however uninstall it from windows by going into the Device Manager (right click inside the Computer folder, system something, link on the left)

I'm using Python 2.7.6

# Usage

Warning! This thing presses the mouse button a lot really fast. TODO: only do this with a command-line option.

It shouldn't move the mouse when you're not interacting with it, but if it goes rouge, just turn off the NXT.

1. Turn on the NXT and connect it to your computer. Duh.
2. Use `sudo python main.py`.
3. You'll probably get a BrickNotFound error or something else. The BrickNotFound error can also mean some things aren't installed. Good luck.
4. Callibration: Follow the instructions. I'd recommend callibrating it a bit lower than, like, whatever... for casual usage? Use `sudo python main.py recallibrate` to do what that command does.


If the ceiling sample is sometimes 255, but sometimes lower, you probably should recallibrate it to its lowest.
Otherwise it will probably mouse the mouse to the top of the screen when you're not interacting with it.


