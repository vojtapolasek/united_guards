#!/usr/bin/env python

import time, random, datetime, cPickle
import ug_globals as glob
from ug_data import *
_ = glob._
#define variables


def position():
	"""sets random positionn of falling sound."""
	global cutplane
	glob.target_falling = True
	glob.previous = time.time()
	glob.rand = random.randrange(0, 3)
	if glob.rand == 0:
		glob.left = 1
		glob.right = 0.1
	elif glob.rand == 1:
		glob.left = 1
		glob.right = 1
	elif glob.rand == 2:
		glob.left = 0.1
		glob.right = 1
	planenum = random.randrange (0, planecount)
	cutplane = soundcut(plane[planenum], glob.orig_delay - glob.delay)
	chan.play(cutplane)
	chan.set_volume(glob.left, glob.right)

def check(input):
	"""checks user input"""
	global cutplane
	if glob.pressed == True: return
	if input == glob.rand and time.time() < glob.previous + glob.delay:
		glob.score += 100 * round ((time.time () - glob.previous), 3)
		missile[input].play ()			
		time.sleep (0.25)
		mgchan.play(planehit)
		mgchan.set_volume(glob.left, glob.right)
		chan.fadeout (200)
		glob.rand=None
		glob.delay -= 0.05
		glob.previous = time.time() + glob.delay * 1.2
		glob.target_falling = False
	else:
		missile[input].play ()
		time.sleep (missile[input].get_length())
		die()
		glob.lives -= 1
		glob.previous = time.time()
		glob.target_falling = False
		glob.previous = time.time() + cutplane.get_length() - (time.time() - glob.previous)
	glob.pressed = True

def die():
	rand = random.randrange (0, mgcount)
	mgchan.play (mg[rand])
	mgchan.set_volume (glob.left, glob.right)
	for i in range (0, 3):
		randvar = random.randrange (0, ricochetcount)
		ricochet[randvar].play()
		time.sleep (0.100)
	for i in range (0, 2):
		randvar = random.randrange (0, bhitcount)
		bhit[randvar].play()
		time.sleep (0.100)
	randvar = random.randrange (0, deadcount)
	dead[randvar].play()

def soundcut (sound, time_to_cut):
	"""Accepts pygame sound object and cuts time_to_cut from its beginning, using numpy array slicing. Returns pygame sound object."""
	length = sound.get_length()
	snd_array = pygame.sndarray.array(sound)
	frame_rate = len(snd_array) / length
	cut_frames = frame_rate * time_to_cut
	result = snd_array [cut_frames:]
	soundresult = pygame.sndarray.make_sound (result)
	return soundresult


def startgame(lives, delay):
	"""starts  game and initialises variables."""
	glob.previous = time.time()
	glob.lives = lives
	glob.orig_delay = glob.delay = delay
	glob.score = 0
	glob.target_falling = False
	glob.rand = None
	glob.remaining = None
	glob.pressed = False
	glob.game_active = True
	glob.menu_active = False
	position()

def gamechecker():
	"""Checks for various game conditions."""
	global cutplane
	if glob.lives <= 0:
		time.sleep(1)
		glob.s.say (_("Game Over. Your final score is {0}.").format(glob.score), 1)
		today = datetime.datetime.today()
		print glob.score
		glob.scoreboard.append([glob.score, today])
		scorefile = open("score.dat", "w")
		cPickle.dump(glob.scoreboard, scorefile)
		scorefile.close()
		print glob.scoreboard
		glob.score = None
		glob.game_active = False
		glob.menu_active = True
		glob.current_menu = glob.main_menu.init()
	if (time.time() >= glob.previous + glob.delay - aim.get_length()) and glob.target_falling == True:
		mgchan.play (aim)
	if (time.time() >= glob.previous + glob.delay) and glob.target_falling == True:
		glob.pressed = True
		mgchan.stop()
		die()
		glob.previous = time.time() + cutplane.get_length() - glob.delay
		glob.lives -=1
		glob.target_falling = False
	elif (time.time() >= glob.previous) and glob.target_falling == False:
		position()
		glob.pressed = False


def pausegame():
	pygame.mixer.pause()
	glob.remaining = time.time() - (glob.previous + glob.delay)
	glob.game_active = False
	glob.menu_active = True
	glob.current_menu = glob.abortprompt.init()


def resumegame():
	glob.previous = time.time() + glob.remaining
	pygame.mixer.unpause()
	glob.game_active = True
	glob.menu_active = False


def abortgame():
	pygame.mixer.stop()
	glob.remaining = None
	glob.score = None
	glob.current_menu = glob.main_menu.init()




