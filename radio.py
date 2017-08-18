#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import RPi.GPIO as GPIO
import subprocess as sp

def control_mpc():
	cr = sp.check_output(["mpc", "playlist"]).split('\n')

	if (len(cr)-1) > control_mpc.pl:
		control_mpc.pl += 1
	else:
		control_mpc.pl = 1
	
	sp.call(["mpc", "play", str(control_mpc.pl)])
	
control_mpc.pl = 1

if __name__ == '__main__':
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	#sp.call(["mpc", "clear", "-q"])
	#sp.call(["mpc", "-q", "load", "all"])
	sp.call(["mpc", "play", "-q"])

	while (1):
		ch = GPIO.wait_for_edge(15, GPIO.RISING)
		control_mpc()
