#!/usr/bin/python3

import pygame

try:
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()
	pygame.init()
	print("loading soudn ...")
	sound = pygame.mixer.Sound("/home/pi/raspiKeys/res/backtracks/processed_wav/house/S_L_127_BEATS_21.wav")
	print("playing sound ...")
	sound.play()

	while True:
		pass

except Exception as e:
	print("ERROR !!!")
	print(e)
