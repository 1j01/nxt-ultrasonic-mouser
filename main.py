#!/usr/bin/env python

from pymouse import PyMouse

mouse = PyMouse()
sw, sh = mouse.screen_size()

def mouse_move(x, y):
	mouse.move(x, y)

def mouse_release():
	mx, my = mouse.position()
	mouse.release(mx, my)

'''
import time
import math
tau = math.pi * 2

for i in range(500):
	x = int(math.sin(tau*i/100)*sw/3 + sw/2)
	y = int(math.cos(tau*i/100)*sh/3 + sh/2)
	mouse_move(x, y)
	time.sleep(.01)
'''

import nxt.locator
from nxt.sensor import *

sock = nxt.locator.find_one_brick()
if sock:
	brick = sock.connect()
	
	# Exit handler
	
	def exit_handler():
		print 'Goodbye!'
		sock.close()
		mouse_release()
	
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
	
	calibrate = not (ceiling_sample and top_sample and bottom_sample)
	if len(sys.argv) > 1:
		a = sys.argv[1]
		if a is 'calibrate' or a is 'recalibrate':
			calibrate = True
	
	if calibrate:
	
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
    
    
    
    
    # This is the actually interesting part
	
	mouse_is_pressed = False
	
	while True:
		current_sample = ultrasonic.get_sample()
		
		x = sw / 2
		y = sh - (sh * (current_sample - bottom_sample) / top_sample)
		
		if current_sample < ceiling_sample - ceiling_threshold_sample:
			print 'Recieved sample!', current_sample, '(Move mouse to y=%s)'%y
			
			# mouse.move(x, y)
			
			if 100 < y < (sh - 100):
				mouse.press(x, y)
				mouse_is_pressed = True
			else:
				mouse.release(x, y)
				mouse_is_pressed = False
		else:
			# print 'Recieved sample!', current_sample, '(Near ceiling)'
			if mouse_is_pressed:
				print 'Releasing mouse'
				mouse_release()
				mouse_is_pressed = False



