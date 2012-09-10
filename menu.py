#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#module for menus
#released on September 03, 2012 by Vojtěch Polášek <vojtech.polasek@gmail.com>

import __main__

items = None
current = None

class menuitem:
	def __init__(self, caption, action):
		self.caption = caption
		self.action = action
	def say(self):
		s.say(self.caption, 1)
	def select(self):
		s.stop()
		exec self.action

class menu:
	def __init__(self,title,items,movesound=None,selectsound=None,bgsound=None):
		self.title = title
		self.items = items
		self.movesound = movesound
		self.selectsound = selectsound
		self.bgsound = bgsound
		self.current = None
	def init(self,current=0):
		self.current = current
		s.say(self.title, 0)
		s.say(self.items[self.current].caption, 0)
		return self
	
	def movedown(self):
		if self.current < len (self.items) -1:
			self.current += 1
		else:
			self.current = 0
		self.items[self.current].say()

	def moveup(self):
		if self.current > 0:
			self.current -= 1
		else:
			self.current = len (self.items) -1
		self.items[self.current].say()
	def select(self):
		self.items[self.current].select()
