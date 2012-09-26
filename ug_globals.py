#!/usr/bin/env python
#module for storing and working with global variables


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
game_active = None #True if game is active
menu_active = None #True if menu is active
current_menu = None #stores current menu
s = None #placeholder for speaker module