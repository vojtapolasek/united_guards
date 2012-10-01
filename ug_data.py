#!/usr/bin/env python
#data for the game united guards


import pygame, os.path, menu, game
pygame.mixer.init()



#initialisation of sounds
plane = []
planecount = 8
for i in range(1, planecount + 1):
	plane.append (pygame.mixer.Sound(os.path.normpath("sounds/plane"+str(i)+".ogg")))
mg = []
mgcount = 9
for i in range(1,mgcount + 1):
	mg.append (pygame.mixer.Sound(os.path.normpath("sounds/mg"+str(i)+".ogg")))
aim = pygame.mixer.Sound(os.path.normpath("sounds/aim.ogg"))
missile = []
for i in range (0, 3):
	missile.append (pygame.mixer.Sound(os.path.normpath("sounds/missile"+str(i)+".ogg")))
planehit = pygame.mixer.Sound (os.path.normpath("sounds/planehit.ogg"))
dead = []
deadcount = 3
for i in range (1, deadcount +1):
	dead.append (pygame.mixer.Sound(os.path.normpath("sounds/dead"+str(i)+".ogg")))
bhit = []
bhitcount = 4
for i in range (1, bhitcount +1):
	bhit.append (pygame.mixer.Sound(os.path.normpath("sounds/bhit"+str(i)+".ogg")))
ricochet = []
ricochetcount =8
for i in range (1, ricochetcount +1):
	ricochet.append (pygame.mixer.Sound(os.path.normpath("sounds/ricoch"+str(i)+".ogg")))

stereotest = pygame.mixer.Sound(os.path.normpath("sounds/stereotest.ogg"))



#channel initialisation
pygame.mixer.set_reserved(2)
chan=pygame.mixer.Channel(0)
mgchan = pygame.mixer.Channel(1)

