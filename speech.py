#!/usr/bin/env python
#simple speech interface for speech dispatcher and windows screenreaders + SAPI
#released on September 03, 2012 by Vojtěch Polášek <vojtech.polasek@gmail.com>
#This is helper module for my software
import sys, gettext, locale


class Speaker:
	"""class for speaking"""
	def init (self):
		if sys.platform.startswith ("linux"):
			import speechd
			self.used = "speechd"
			self.s = speechd.Speaker("pyspeech", "pyspeech")
			self.say = self.spdSpeak
			self.stop = self.s.cancel
			lang = []
			fullang, enc = locale.getdefaultlocale()
			lang.append(fullang.split("_")[0])
			if gettext.find("messages", "lang", lang) != None:
				self.s.set_language(lang[0])
		elif sys.platform == "win32":
			import ctypes
			self.used = "srapi"
			self.s = ctypes.windll.ScreenreaderAPI
			self.s.sapiEnable(1)
			self.say = self.s.sayStringW
			self.stop = self.s.stopSpeech
	def spdSpeak(self, text, interrupt):
		if interrupt == 1:
			self.s.cancel()
			self.s.speak(text)
		elif interrupt == 0:
			self.s.speak(text)

	def quit(self):
		if self.used == "speechd":
			self.s.close()

def getTransFunc():
	locale.setlocale(locale.LC_ALL, '')
	lang = []
	fullang, enc = locale.getdefaultlocale()
	lang.append(fullang.split("_")[0])
	trans = gettext.translation("messages", "lang", lang, fallback=True, codeset=enc)
	_ = trans.ugettext
	return _
