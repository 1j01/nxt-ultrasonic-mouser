#!/usr/bin/env python

'''
import ctypes
user32 = ctypes.windll.user32
sw = screen_width = user32.GetSystemMetrics(0)
sh = screen_height = user32.GetSystemMetrics(1)

def mouse_move(x, y):
	user32.SetCursorPos(x, y)

def mouse_down():
	ctypes.windll.user32.mouse_event(2, 0, 0, 0,0)

def mouse_up():
	ctypes.windll.user32.mouse_event(4, 0, 0, 0,0)

'''

import pymouse
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

	import atexit
	
	def exit_handler():
		print 'Goodbye!'
		sock.close()
		mouse_release()

	atexit.register(exit_handler)

	# Info
	
	name, host, signal_strength, user_flash = brick.get_device_info()
	print ''
	print 'NXT brick name: %s' % name
	print 'Host address: %s' % host
	print 'Bluetooth signal strength: %s' % signal_strength
	print 'Free user flash: %s' % user_flash
	print ''
	print 'Okay!'
	
	# Ultrasonic Sensor
	
	ultrasonic = UltrasonicSensor(brick, PORT_4)
	
	# <Callibration>
	
	from ConfigParser import *

	config = SafeConfigParser()
	config.read('callibration.ini')
	
	ceiling_sample = None
	top_sample = None
	bottom_sample = None
	
	try:
		ceiling_sample = config.getint('Callibration', 'ceiling')
		top_sample = config.getint('Callibration', 'top')
		bottom_sample = config.getint('Callibration', 'bottom')
	except Exception:
		pass
	
	import sys
	
	callibrate = not (ceiling_sample and top_sample and bottom_sample)
	if len(sys.argv) > 1:
		a = sys.argv[1]
		if (a == 'callibrate') or (a == 'recallibrate'):
			callibrate = True
	
	if callibrate:
	
		print 'Begin callibration. Place the brick in front of your monitor with the Ultrasonic Sensor facing upwards.'
	
	
		raw_input('Press Enter when you have the Ultrasonic Sensor sensing the distance to the ceiling.')
		ceiling_sample = ultrasonic.get_sample()
		print 'Ceiling at %s' % ceiling_sample
	
		raw_input('Place your hand over the sensor level with the bottom of your screen. Press Enter.')
		bottom_sample = ultrasonic.get_sample()
		print 'Bottom of screen at %s' % bottom_sample
	
		raw_input('Move your hand to the top of your screen. Press Enter to finish callibration.')
		top_sample = ultrasonic.get_sample()
		print 'Top of screen at %s' % top_sample
		
		# Write the callibration configuration to a file
		
		# This is WAY more complicated than it needs to be.
		try:
			config.add_section('Callibration')
		except DuplicateSectionError:
			pass
		
		config.set('Callibration', 'ceiling', str(ceiling_sample))
		config.set('Callibration', 'top', str(top_sample))
		config.set('Callibration', 'bottom', str(bottom_sample))
		# config['Callibration']['ceiling'] = ceiling_sample
		# config['Callibration']['top'] = top_sample
		# config['Callibration']['bottom'] = bottom_sample
		with open('callibration.ini', 'w') as config_file:
			config.write(config_file)
		# That was ridiculously tedious
	
	# </Callibration>
	
	# This is the threshold below the recorded ceiling distance below which new samples are considered interaction-y
	ceiling_threshold_sample = 30
    
    
    
    
    # This is the actually interesting part
	
	mouse_is_pressed = False
	
	while True:
		current_sample = ultrasonic.get_sample()
		
		x = sw / 2
		y = sh - (sh * (current_sample - bottom_sample) / top_sample)
		
		if current_sample < ceiling_sample - ceiling_threshold_sample:
			print 'Recieved sample!', current_sample, '(Move mouse to y =', y, ')'
			
			# mouse.move(x, y)
			
			if 100 < y < (sh - 100):
				mouse.press(x, y)
				mouse_is_pressed = True
			else:
				mouse.release(x, y)
				mouse_is_pressed = False
		else:
			#print 'Recieved sample!', current_sample, '(Near ceiling)'
			if mouse_is_pressed:
				print 'Releasing mouse'
				mouse_release()
				mouse_is_pressed = False
		
	
	
# 	sock.close()
# else:
# 	print 'no sock, no brick; no brick, no fun'
