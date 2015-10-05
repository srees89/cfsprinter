"""
pyttsx (text to speech)
Copyright 2014 Shane Rees <https://github.com/Shaggs/>

This plug-in is designed to read out a copy of the received turnout
Page for those that maybe in the station or form those coming in
and need details.

it reads only parts of the page. They are RESPOND (job type), Alarm Level,
address, and any extra info after the ==

the speed is hard coded at this stage.



This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import absolute_import
from . import BasePlugin
import pyttsx
import re
import time
import threading
import os.path
import pygame
import string
from pagerprinter.misc.abbreviations import abbreviations

pygame.mixer.init()
pygame.init()
engine = pyttsx.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 120)
volume = engine.getProperty('volume')
engine.setProperty('volume', 150)
o = os.path.join('pagerprinter', 'sounds', 'alert.wav')
s = pygame.mixer.Sound(o)


class TTS(BasePlugin):
	def say(self, resp, info, address, appliance):
		if resp:
			for group in resp.groups():
				if info:
					for group2 in info.groups():
						if appliance:
							for group3 in appliance.groups():
								for x in range(3):
									s.play()
									time.sleep(6)
									engine.say(group)
									engine.say(group2)
									engine.say(address)
									engine.say(group3)
									engine.runAndWait()
									time.sleep(20)

	def execute(self, msg, unit, address, when, printer, print_copies):
		pattern = re.compile(r'\b(' + '|'.join(abbreviations.keys()) + r')\b')
		msg = pattern.sub(lambda x: abbreviations[x.group()], msg)
		res = str('%s - %s' % (msg, unit))
		rem = re.compile('.*(RESPOND.*?ALARM\sLEVEL:\s\d)')
		resp = rem.match(res)
		more = str('%s - %s - %s' % (address, msg, unit))
		inf = re.compile('.*==(.*?\s:)')
		info = inf.match(more)
		app = re.compile('.*:(.*?\s:\s-)')
		appliance = app.match(more)
		address = re.sub(r'#\d{3}/\d{3}|@|\s:\s', '', address)
		my_thread = threading.Thread(target=self.say, args=(resp, info, address, appliance))
		my_thread.start()
PLUGIN = TTS
