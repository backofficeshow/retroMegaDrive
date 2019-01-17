#!/usr/bin/env python
#retroMegaDrive
#(c)2019 Dr A @Backofficeshow
#TODO; work on the threads, this is first time in python and not bad for a couple of hours, but im not happy yet :)

import sys
sys.path.append('/home/pi/MFRC522-python')
import RPi.GPIO as GPIO
import SimpleMFRC522
import os
import subprocess
import time
import threading

reader = SimpleMFRC522.SimpleMFRC522()
title = ""
stopping = 0
oldswi = 99
power = 0
splash = 0

def read_from_card():
	global ready
	global title
	ready = 0
	while stopping == 0:
		print("Waiting for card")
		id, title = reader.read_no_block()
		while not id:
	     		id, title = reader.read_no_block()
			time.sleep(0.1)
		print("Card " + title + " found")
		ready = 1
		while ready == 1:
			time.sleep(0.1)
	print("Card Process DONE")

def logo(state):
	try:
		os.killpg(os.getpgid(splash.pid), signal.SIGTERM)
	except NameError:
		print("No splash")

	if state == 1:
		splash=subprocess.Popen('fbi /home/pi/logoON.jpg -noverbose -a', shell=True)
	else:
		splash=subprocess.Popen('fbi /home/pi/logoOFF.jpg -noverbose -a', shell=True)

try:
	GPIO.setup(24,GPIO.OUT)
	GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	thread = threading.Thread(target=read_from_card)
	
	print("We Begin")
	thread.start()
	while True:
		inputswi = GPIO.input(23)
		if ready == 1:
			if power == 1:
				print('Loading emulator')
				os.system('killall retroarch -q')
				p=subprocess.Popen('nohup /home/pi/romLoader.sh ' + title, shell=True)
			ready = 0

		if inputswi != oldswi:
			print("Switch used")
			if inputswi == 0:
				print("Poweroff")
				GPIO.output(24, GPIO.LOW)
				os.system('killall retroarch -q')
				logo(0)
				power = 0
			else:
				print("Poweron")
				GPIO.output(24, GPIO.HIGH)
				logo(1)
				power = 1
			oldswi = inputswi
		time.sleep(0.1)
		 
		
finally:
	stopping = 1
	GPIO.cleanup()

