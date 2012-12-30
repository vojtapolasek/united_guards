#!/usr/bin/env python
#menus are defined here
import game, pygame, menu, sys, time, speech, cPickle
from ug_data import *
s = speech.s
_ = speech.getTransFunc()







def resumegame():
	ev_game_active = pygame.event.Event(pygame.USEREVENT, {'code': 1})
	game.previous = time.time() + game.remaining
	pygame.mixer.unpause()
	pygame.event.post(ev_game_active)


def abortgame():
	pygame.mixer.stop()
	game.remaining = None
	game.score = None
	return main_menu.init()


def quit ():
	s.say (_("Exiting now."), 1)
	s.quit ()
	pygame.quit ()
	sys.exit ()

def readmanual():
	s.say (_("This is very simple. Listen for incoming planes and press corresponding arrow (Left, Up or Right) to launch a missile in given direction.\nPress L to announce number of remaining lives and S to announce your score.\nPress ESCAPE to pause the game.\nHave fun!"), 1)

#define function for dynamic generation of score menu
def genscoremenu(field):
 	scoremenuitems = []
	filteredscore = []
	for score in game.scoreboard:
		if score[field] != None:
			filteredscore.append(score) 
	if field == 0:
		sortedscore = sorted(filteredscore, key = lambda score: score[field], reverse=True)
	else:
		sortedscore = sorted(filteredscore, key = lambda score: score[field])
 	for item in sortedscore:
		menustring = _("{0} points").format(item[0])+unicode(time.strftime("%c", item[1]), "utf-8")
		if item[2] != None:
			menustring += _(", the fastest reaction {0} milliseconds").format(item[2])
 		scoremenuitems.append(menu.menuitem(menustring, None))
 	scoremenuitems.append(menu.menuitem(_("Go back"), lambda :main_menu.init()))
 	scoremenu = menu.menu(_("Use up and down arrows to browse score.\nSelect last item to return to the main menu."), scoremenuitems)
 	return scoremenu.init()

def stereoTestFunc():
	game.chan.play(stereotest)

def resetScoreFunc():
	game.scoreboard = []
	scorefile = open("score.dat", "w")
	cPickle.dump (game.scoreboard, scorefile)
	scorefile.close()
	s.say(_("The score has been reset."), 1)
#define menus
#define main menu
start = menu.menuitem(_("Start the game"), game.startgame, [5, 3])
testspeakers = menu.menuitem(_("Test your speakers"), stereoTestFunc)
viewscore = menu.menuitem(_("View your score"), genscoremenu, [0])
resetscore =menu.menuitem(_("Reset your score"), resetScoreFunc)
instructions = menu.menuitem(_("Read instructions"), readmanual)
quit = menu.menuitem(_("Quit the game"), quit)
main_menu = menu.menu(_("Welcome to the main menu. Use up and down arrows to select an item, enter to confirm and escape to quit."), [start, testspeakers, viewscore, resetscore, instructions, quit])
#define pause game prompt
continuegame = menu.menuitem(_("Continue the game"), resumegame)
abort = menu.menuitem(_("Abort the game and return to the main menu."), abortgame)
abortprompt = menu.menu(_("Do you really want to abort the game?"), [continuegame, abort])

