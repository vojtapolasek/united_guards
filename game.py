#!/usr/bin/env python
#game functions for united guards
import time, random, datetime, cPickle, speech
_ = speech.getTransFunc()
s = speech.s
from ug_data import *

#define variables

lives = None #number of lives
delay = None #delay between planes 
orig_delay = None
rand = None  #used in generating of direction and checking user input
score = None
scoreboard = None
target_falling = None  #True when attack is pending
previous = None  #stores last needed time
remaining = None #stores time when game is paused
paused = False
pressed = False
left = None #volume for incoming plane
right = None #the same as above
ev_game_ended = pygame.event.Event(pygame.USEREVENT, {"code": 3})
ev_game_active = pygame.event.Event(pygame.USEREVENT, {'code': 1})


def position():
	"""sets random positionn of falling sound."""
	global cutplane, target_falling, previous, orig_delay, delay, left, right, rand
	target_falling = True
	previous = time.time()
	rand = random.randrange(0, 3)
	if rand == 0:
		left = 1
		right = 0.1
	elif rand == 1:
		left = 1
		right = 1
	elif rand == 2:
		left = 0.1
		right = 1
	planenum = random.randrange (0, planecount)
	cutplane = soundcut(plane[planenum], orig_delay - delay)
	chan.play(cutplane)
	chan.set_volume(left, right)

def check(input):
	"""checks user input"""
	global cutplane, pressed, rand, delay, previous, target_falling, lives, left, right, score
	if pressed == True: return
	if input == rand and time.time() < previous + delay:
		score += 100 * round ((time.time () - previous), 3)
		missile[input].play ()			
		time.sleep (0.25)
		mgchan.play(planehit)
		mgchan.set_volume(left, right)
		chan.fadeout (200)
		rand=None
		delay -= 0.05
		previous = time.time() + delay * 1.2
		target_falling = False
	else:
		missile[input].play ()
		time.sleep (missile[input].get_length())
		die()
		lives -= 1
		previous = time.time()
		target_falling = False
		previous = time.time() + cutplane.get_length() - (time.time() - previous)
	pressed = True
	return lives, score, previous, pressed, target_falling

def die():
	global left, right
	rand = random.randrange (0, mgcount)
	mgchan.play (mg[rand])
	mgchan.set_volume (left, right)
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


def startgame(clives, cdelay):
	"""starts  game and initialises variables."""
	global lives, delay, orig_delay, previous, score
	previous = time.time()
	lives = clives
	orig_delay = delay = cdelay
	score = 0
	pygame.event.post(ev_game_active)
	position()



def gamechecker():
	"""Checks for various game conditions."""
	global cutplane, lives, score, previous, delay, target_falling, pressed
	if lives <= 0:
		time.sleep(1)
		s.say (_("Game Over. Your final score is {0}.").format(score), 1)
		scoreboard.append([score, time.localtime()])
		scorefile = open("score.dat", "w")
		cPickle.dump(scoreboard, scorefile)
		scorefile.close()
		score = None
		pygame.event.post(ev_game_ended)
		return
	if (time.time() >= previous + delay - aim.get_length()) and target_falling == True:
		mgchan.play (aim)
	if (time.time() >= previous + delay) and target_falling == True:
		pressed = True
		mgchan.stop()
		die()
		previous = time.time() + cutplane.get_length() - delay
		lives -=1
		target_falling = False
	elif (time.time() >= previous) and target_falling == False:
		position()
		pressed = False

def pausegame():
	global remaining, previous, delay
	ev_game_paused = pygame.event.Event(pygame.USEREVENT, {"code": 2})
	pygame.mixer.pause()
	remaining = time.time() - (previous + delay)
	pygame.event.post(ev_game_paused)
