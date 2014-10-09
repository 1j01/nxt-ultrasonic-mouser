#!/usr/bin/env python

# The interesting part is at the bottom!

from __future__ import division,  print_function

# Parse command line arguments

import argparse

parser = argparse.ArgumentParser(
	description='NXT Ultrasonic Mouser',
	formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('-d', '--direction', action='store', default='up', choices=['left', 'right', 'up', 'down'], help='the direction the sensor is pointing across the screen')
parser.add_argument('-r', '--recalibrate', action='store_true', help='recalibrate the sensor to the screen')
parser.add_argument('-c', '--clicky', action='store_true', help='auto-click repeatedly while interacting')
parser.add_argument('-b', '--bounds', action='store_true', help='choose the on-screen bounds for auto-clicking')
parser.add_argument('-w', '--swirly', action='store_true', help=';)')

args = vars(parser.parse_args())

closer_edge = {
	'left': 'right',
	'right': 'left',
	'up': 'bottom',
	'down': 'top'
}[args['direction']]

further_edge = {
	'left': 'left',
	'right': 'right',
	'up': 'top',
	'down': 'bottom'
}[args['direction']]

# Set up mouse emulation

from pymouse import PyMouse

mouse = PyMouse()
screen_width, screen_height = mouse.screen_size()

# Set up additional mouse abstraction

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


# ;)

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
		print('Disconnecting NXT socket')
		sock.close()
		print('Releasing mouse')
		mouse_release()
	
	import atexit
	atexit.register(exit_handler)
	
	# Print brick info
	
	name, host, signal_strength, user_flash = brick.get_device_info()
	print('')
	print('NXT brick name:', name)
	print('Host address:', host)
	print('Bluetooth signal strength:', signal_strength)
	print('Free user flash:', user_flash)
	print('')
	
	# Ultrasonic Sensor
	
	ultrasonic = UltrasonicSensor(brick, PORT_4)
	
	# Calibration
	
	config_file_name = 'config.ini'
	
	from ConfigParser import *

	config = SafeConfigParser()
	config.read(config_file_name)
	
	ceiling_sample = None
	upper_sample = None
	lower_sample = None
	
	try:
		ceiling_sample = config.getint('Calibration', 'ceiling')
		upper_sample = config.getint('Calibration', 'upper')
		lower_sample = config.getint('Calibration', 'lower')
	except Exception:
		pass
	
	import sys
	
	if args['recalibrate'] or not (ceiling_sample and upper_sample and lower_sample):
		
		print('Begin calibration.')
		
		def input_sample(prompt, display):
			# Todo: interactive display until input
			raw_input(prompt)
			sample = ultrasonic.get_sample()
			print(display.format(sample))
			return sample
		
		ceiling_sample = input_sample('Press Enter to record the distance when you aren\'t interacting with the sensor.', 'Ceiling sample: {0}')
		
		if ceiling_sample is 255:
			print('Warning: 255 means the distance is far away (which is good), but it can cause issues if it fluctuates between 255 and something much lower. If it moves your mouse to the edge of the screen when you aren\'t interacting with it, recalibrate and see if you can get a lower number.')
		
		lower_sample = input_sample('Place your hand over the sensor level with the %s edge of your screen. Press Enter.' % closer_edge, 'Lower sample: {0}')
		
		if lower_sample is 255:
			print('Abort: 255 means the distance is out of range of your sensor (too far away!)')
			sys.exit(1)
		
		upper_sample = input_sample('Move your hand to the %s edge of your screen. Press Enter to finish calibration.' % further_edge, 'Upper sample: {0}')
		
		if upper_sample is 255:
			print('Abort: 255 means the distance is out of range of your sensor (too far away!)')
			sys.exit(1)
		
		
		
		# Write the configuration to a file
		try:
			config.add_section('Calibration')
		except DuplicateSectionError:
			pass
		
		config.set('Calibration', 'ceiling', str(ceiling_sample))
		config.set('Calibration', 'upper', str(upper_sample))
		config.set('Calibration', 'lower', str(lower_sample))
		
		with open(config_file_name, 'w') as config_file:
			config.write(config_file)
		
	# End Calibration
	
	
	# The threshold below the recorded ceiling distance within which new samples are also considered ceiling
	ceiling_threshold_sample = 30
    
    
    
    
    # Here comes the interesting part
	
	while True:
		
		try:
			current_sample = ultrasonic.get_sample()
		except nxt.error.DirProtError:
			print('')
			print('(!) nxt.error.DirProtError: Communication bus error')
			brick = sock.connect()
			print('($) Reconnected')
			print('')
			pass
		except KeyboardInterrupt:
			print('')
			sys.exit(0)
		
		
		
		x = screen_width / 2
		y = screen_height / 2
		
		# when current_sample = upper_sample, sample_ratio should = 1
		# when current_sample = lower_sample, sample_ratio should = 0
		sample_ratio = (current_sample - lower_sample) / (upper_sample - lower_sample)
		
		if args['direction'] == 'left':
			# Pointin' to da left
			x = screen_width * (1 - sample_ratio)
		elif args['direction'] == 'right':
			# Pointin' to da right
			x = screen_width * sample_ratio
		elif args['direction'] == 'up':
			# Pointing up
			y = screen_height * (1 - sample_ratio)
		else:
			# Are you hanging this from the ceiling or something? Okay...
			y = screen_height * sample_ratio
		
		
		
		def print_status(format_string):
			text = format_string.format(
				sample=current_sample,
				us=upper_sample,
				ls=lower_sample,
				percent=int(sample_ratio*100),
				x=int(x), y=int(y)
			)
			sys.stdout.write('\r\x1b[K' + text)
			sys.stdout.flush()
		
		if current_sample < ceiling_sample - ceiling_threshold_sample:
			
			print_status('sample: {us} > ({sample}) > {ls}, {percent}%, move mouse to ({x}, {y})')
			
			if args['clicky']:
				if 100 < y < (screen_height - 100):
					mouse_press(x, y)
					mouse_release(x, y)
				else:
					mouse_release(x, y)
			else:
				mouse_move(x, y)
			
		else:
			
			print_status('sample: {us} > ({sample}) > {ls}, {percent}%, (near ceiling)')
			
			if mouse_is_pressed:
				mouse_release()


