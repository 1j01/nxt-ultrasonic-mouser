#!/usr/bin/env python

# The interesting part is at the bottom!



# Parse command line arguments

import argparse

parser = argparse.ArgumentParser(
	description='Be awesome. NXT Ultrasonic Mouser',
	formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('-r', '--recalibrate', action='store_true', help='Recalibrate the sensor to the screen')
parser.add_argument('-x', '--horizontal', action='store_true', help='Use horizontal mode (point sensor across screen to the right)')
parser.add_argument('-c', '--clicky', action='store_true', help='Auto-click repeatedly while interacting')
parser.add_argument('-b', '--bounds', action='store_true', help='Choose the on-screen bounds for auto-clicking')
parser.add_argument('-w', '--swirly', action='store_true', help=';)')

args = vars(parser.parse_args())

# Set up mouse emulation

from pymouse import PyMouse

mouse = PyMouse()
screen_width, screen_height = mouse.screen_size()

# Set up mouse abstraction

mouse_is_pressed = False
mouse_last_x = screen_width / 2
mouse_last_y = screen_height / 2

def mouse_coords(x = None, y = None):
	
	global mouse_last_x
	global mouse_last_y
	
	if x is None or y is None:
		# Retrieving the mouse position for some reason causes "Communication bus error"s
		# x, y = mouse.position()
		x = mouse_last_x
		y = mouse_last_y
	else:
		mouse_last_x = x
		mouse_last_y = y
	
	return x, y

def mouse_move(x, y):
	mouse_coords(x, y)
	mouse.move(x, y)

def mouse_press(x = None, y = None):
	global mouse_is_pressed
	x, y = mouse_coords(x, y)
	mouse.press(x, y)
	mouse_is_pressed = True

def mouse_release(x = None, y = None):
	global mouse_is_pressed
	x, y = mouse_coords(x, y)
	mouse.release(x, y)
	mouse_is_pressed = False


#    ;)

if args['swirly']:
	import time
	import math
	tau = math.pi * 2

	for i in range(500):
		x = int(math.sin(tau*i/100)*screen_width/3 + screen_width/2)
		y = int(math.cos(tau*i/100)*screen_height/3 + screen_height/2)
		mouse_move(x, y)
		time.sleep(.01)
	
	parser.exit()

# Connect to the NXT

import nxt.locator
from nxt.sensor import *

sock = nxt.locator.find_one_brick()
if sock:
	brick = sock.connect()
	
	# Exit handler
	
	def exit_handler():
		print 'Disconnecting NXT socket'
		sock.close()
		print 'Releasing mouse'
		mouse_release()
		print 'All good things must come to a brutal end'
	
	import atexit
	atexit.register(exit_handler)
	
	# Info
	
	name, host, signal_strength, user_flash = brick.get_device_info()
	print ''
	print 'NXT brick name:', name
	print 'Host address:', host
	print 'Bluetooth signal strength:', signal_strength
	print 'Free user flash:', user_flash
	print ''
	print 'Okay!'
	
	# Ultrasonic Sensor
	
	ultrasonic = UltrasonicSensor(brick, PORT_4)
	
	# <Calibration>
	
	config_file_name = 'config.ini'
	
	from ConfigParser import *

	config = SafeConfigParser()
	config.read(config_file_name)
	
	ceiling_sample = None
	top_sample = None
	bottom_sample = None
	
	try:
		ceiling_sample = config.getint('Calibration', 'ceiling')
		top_sample = config.getint('Calibration', 'top')
		bottom_sample = config.getint('Calibration', 'bottom')
	except Exception:
		pass
	
	import sys
	
	if args['recalibrate'] or not (ceiling_sample and top_sample and bottom_sample):
	
		print 'Begin calibration. Place the brick in front of your monitor with the Ultrasonic Sensor facing upwards.'
	
	
		raw_input('Press Enter when you have the Ultrasonic Sensor sensing the distance to the ceiling.')
		ceiling_sample = ultrasonic.get_sample()
		print 'Ceiling at', ceiling_sample
		
		if ceiling_sample is 255:
			print 'Warning: 255 means the distance is far away (which is generally good), but it can cause issues if it fluctuates between 255 and something like 143. If it moves your mouse to the top of the screen when you aren\'t interacting with it, recalibrate and see if you can get a lower number.'
	
		raw_input('Place your hand over the sensor level with the bottom of your screen. Press Enter.')
		bottom_sample = ultrasonic.get_sample()
		print 'Bottom of screen at', bottom_sample
	
		raw_input('Move your hand to the top of your screen. Press Enter to finish calibration.')
		top_sample = ultrasonic.get_sample()
		print 'Top of screen at', top_sample
		
		
		# Write the configuration to a file
		# This is WAY more complicated than it needs to be.
		try:
			config.add_section('Calibration')
		except DuplicateSectionError:
			pass
		
		config.set('Calibration', 'ceiling', str(ceiling_sample))
		config.set('Calibration', 'top', str(top_sample))
		config.set('Calibration', 'bottom', str(bottom_sample))
		# config['Calibration']['ceiling'] = ceiling_sample
		# config['Calibration']['top'] = top_sample
		# config['Calibration']['bottom'] = bottom_sample
		
		with open(config_file_name, 'w') as config_file:
			config.write(config_file)
		
		# That was ridiculously tedious
	
	# </Calibration>
	
	
	# The threshold below the recorded ceiling distance below which new samples are considered interaction
	ceiling_threshold_sample = 30
    
    
    
    
    # This is the interesting part
	
	while True:
		
		current_sample = ultrasonic.get_sample()
		
		x = screen_width / 2
		y = screen_height / 2
		
		if args['horizontal']:
			x = screen_width - (screen_width * (current_sample - bottom_sample) / top_sample)
		else:
			y = screen_height - (screen_height * (current_sample - bottom_sample) / top_sample)
		
		if current_sample < ceiling_sample - ceiling_threshold_sample:
			print current_sample, '(Move mouse to y=%s)' % y
			
			if args['clicky']:
				if 100 < y < (screen_height - 100):
					mouse_press(x, y)
				else:
					mouse_release(x, y)
			else:
				mouse_move(x, y)
			
		else:
			# print current_sample, '(Near ceiling)'
			
			if mouse_is_pressed:
				print 'Releasing mouse'
				mouse_release()



