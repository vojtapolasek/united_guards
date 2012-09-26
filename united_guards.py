#!/usr/bin/env python
#version 0.3, released on September 26, 2012 by Vojtech Polasek <vojtech.polasek@gmail.com>
# the game is structured into several modules:
#game - game functions
# ug_data - various declarations that won't change
# ug_globals - often changing variables which need to be accessed from several modules - couldn't think about better solution
# speech - module for speech
# menu - module for creating menus
#see included README file for more info

#initialisation

import time, pygame, os.path, random, speech, sys, cPickle, datetime, gettext, locale
import ug_globals as glob
#pygame initialisation
pygame.init()
pygame.display.set_mode((320, 200))
pygame.display.set_caption ('United guards')

#initialisation of speech
glob.s =speech.Speaker()
glob.s.init()
#gettext initialisation
lang = []
fullang, enc = locale.getdefaultlocale()
lang.append(fullang.split("_")[0])
trans = gettext.translation("messages", "lang", lang, fallback=True, codeset=enc)
glob._ = trans.ugettext
if gettext.find("messages", "lang", lang) != None and glob.s.used == "speechd":
	glob.s.set_language(lang[0])
_ = glob._


import game, menu



loop_running = None #True if main loop catching events is running



#define some other functions



def loop():
	"""main loop catching keyboard and other events."""
	loop_running = True
	while loop_running == True:
		pygame.time.wait(1)
		event = pygame.event.poll ()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if glob.game_active == True:
					game.pausegame()
			elif event.key ==  pygame.K_RETURN:
				if glob.menu_active == True:
					glob.current_menu.select()
			elif event.key == pygame.K_LEFT:
				if glob.game_active == True:
					game.check(0)
			elif event.key == pygame.K_UP:
				if glob.menu_active == True:
					glob.current_menu.moveup()
				elif glob.game_active == True:
					game.check(1)
			elif event.key == pygame.K_RIGHT:
				if glob.game_active == True:
					game.check(2)
			elif event.key == pygame.K_DOWN:
				if glob.menu_active == True:
					glob.current_menu.movedown()
			elif event.key == pygame.K_s:
				if glob.game_active == True:
					glob.s.say(_("Your score is {0}.").format(glob.score), 1)
			elif event.key == pygame.K_l:
				if glob.game_active == True:
					glob.s.say (_("You have {0} lives remaining.").format(glob.lives), 1)
			elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
				glob.s.stop()
		if glob.game_active == True:
			game.gamechecker()


def quit ():
	glob.s.say (_("Exiting now."), 1)
	glob.s.quit ()
	pygame.quit ()
	sys.exit ()

def readmanual():
	glob.s.say (_("This is very simple. Listen for incoming planes and press corresponding arrow (Left, Up or Right) to launch a missile in given direction.\nPress L to announce number of remaining lives and S to announce your score.\nPress ESCAPE to pause the game.\nHave fun!"), 1)

def mainmenufunc():
	glob.current_menu = glob.main_menu.init()
#define function for dynamic generation of score menu
def genscoremenu():
 	scoremenuitems = []
 	for item in glob.scoreboard:
 		scoremenuitems.append(menu.menuitem(_("{0} points").format(item[0])+str(item[1].strftime(locale.nl_langinfo(locale.D_T_FMT))), None))
 	scoremenuitems.append(menu.menuitem(_("Go back"), mainmenufunc))
 	scoremenu = menu.menu(_("Use up and down arrows to browse score.\nSelect last item to return to the main menu."), scoremenuitems)
 	glob.current_menu = scoremenu.init()

def resetScoreFunc():
	glob.scoreboard = []
	scorefile = open("score.dat", "w")
	cPickle.dump (glob.scoreboard, scorefile)
	scorefile.close()
#define menus
#define main menu
start = menu.menuitem(_("Start the game"), game.startgame, [5, 3])
viewscore = menu.menuitem(_("View your score"), genscoremenu)
resetscore =menu.menuitem(_("Reset your score"), resetScoreFunc) 
instructions = menu.menuitem(_("Read instructions"), readmanual)
quit = menu.menuitem(_("Quit the game"), quit)
main_menu = menu.menu(_("Welcome to the main menu. Use up and down arrows to select an item, enter to confirm and escape to quit."), [start, viewscore, resetscore, instructions, quit])
glob.main_menu = main_menu
#define pause game prompt
continuegame = menu.menuitem(_("Continue the game"), game.resumegame)
abort = menu.menuitem(_("Abort the game and return to the main menu."), game.abortgame)
abortprompt = menu.menu(_("Do you really want to abort the game?"), [continuegame, abort])
glob.abortprompt = abortprompt







if __name__ == "__main__":
	from ug_data import *
	glob.s.say(_("Welcome to the game."), 1)
	glob.current_menu = main_menu.init()
	glob.menu_active = True
	try:
		scorefile = open("score.dat", "r")
		try:
			glob.scoreboard = cPickle.load(scorefile)
		except EOFError:
			glob.scoreboard = []
		scorefile.close()
	except IOError:
		glob.scoreboard = []
		scorefile = open("score.dat", "w")
		scorefile.close()
		print glob.scoreboard
	loop()
