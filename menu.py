#!/usr/bin/env python
#module for menus
# last changes on September 25. 2012 by Vojtech Polasek <vojtech.polasek@gmail.com>
import ug_globals as glob

items = None


class menuitem:
	def __init__(self, caption, action,args=None):
		self.caption = caption
		self.action = action
		self.args = args
	def say(self):
		glob.s.say(self.caption, 1)
	

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
		glob.s.say(self.title, 0)
		glob.s.say(self.items[self.current].caption, 0)
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
		glob.s.stop()
		if self.items[self.current].action == None:
			return
		if self.items[self.current].args == None:
			self.items[self.current].action()
		else:
			self.items[self.current].action (*self.items[self.current].args)
