#!/usr/bin/env python
#version 0.3, released on September 26, 2012 by Vojtech Polasek <vojtech.polasek@gmail.com>
# the game is structured into several modules:
#game - game functions
# ug_data - various declarations that won't change
# speech - module for speech
# menu - module for creating menus
#see included README file for more info

#initialisation

import time, pygame, os.path, random, speech, sys, cPickle
#pygame initialisation
pygame.init()
pygame.display.set_mode((320, 200))
pygame.display.set_caption ('United guards')

#initialisation of speech
s =speech.Speaker()
s.init()
speech.s = s
_ = speech.getTransFunc()



import game, menu, menus




loop_running = None #True if main loop catching events is running
game_active = None
menu_active = None
current_menu = None




def loop():
	"""main loop catching keyboard and other events."""
	global game_active, menu_active, current_menu
	loop_running = True
	while loop_running == True:
		pygame.time.wait(1)
		event = pygame.event.poll ()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if game_active == True:
					game.pausegame()
			elif event.key ==  pygame.K_RETURN:
				if menu_active == True:
					returned = current_menu.select()
					if returned != None:
						current_menu = returned
			elif event.key == pygame.K_LEFT:
				if game_active == True:
					game.check(0)
			elif event.key == pygame.K_UP:
				if menu_active == True:
					current_menu.moveup()
				elif game_active == True:
					game.check(1)
			elif event.key == pygame.K_RIGHT:
				if game_active == True:
					game.check(2)
			elif event.key == pygame.K_DOWN:
				if menu_active == True:
					current_menu.movedown()
			elif event.key == pygame.K_s:
				if game_active == True:
					s.say(_("Your score is {0}.").format(game.score), 1)
			elif event.key == pygame.K_l:
				if game_active == True:
					s.say (_("You have {0} lives remaining.").format(game.lives), 1)
			elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
				s.stop()
		if event.type == pygame.USEREVENT:
			if event.code == 1:
				game_active = True
				menu_active = False
			if event.code == 2:
				game_active = False
				menu_active = True
				current_menu = menus.abortprompt.init()
			if event.code == 3:
				game_active = False
				menu_active = True
				current_menu = menus.main_menu.init()
		if game_active == True:
			game.gamechecker()







if __name__ == "__main__":
	from ug_data import *
	s.say(_("Welcome to the game."), 1)
	current_menu = menus.main_menu.init()
	menu_active = True
	try:
		scorefile = open("score.dat", "r")
		try:
			game.scoreboard = cPickle.load(scorefile)
		except EOFError:
			game.scoreboard = []
		scorefile.close()
	except IOError:
		game.scoreboard = []
		scorefile = open("score.dat", "w")
		scorefile.close()
	loop()
