#!/usr/bin/env python
"""
Directions Via Gmaps.
Copyright 2015 Shane Rees <http://github.com/Shaggs/>

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
from traceback import print_exc
import json, urllib, re
from urllib import urlencode


try:
	from win32api import ShellExecute
except ImportError, ex:
	print_exc()
	print "NOTICE: directions could not be loaded on this platform."
	PLUGIN = None
else:
	from tempfile import mktemp

	class directions(BasePlugin):
		def configure(self, c):
			# read in phone numbers we need
				self.home = c.get('pagerprinter', 'home')
		"""This plugin prints out a text document on Windows of the details."""
		def execute(self, msg, unit, address, when, printer, print_copies):
			url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
				('origin', self.home),
				('destination', address)
			))
			ur = urllib.urlopen(url)
			result = json.load(ur)

			filename = mktemp('.txt')
			with open(filename, 'w') as output:
				for i in range(0, len(result['routes'][0]['legs'][0]['steps'])):
					s = (result['routes'][0]['legs'][0]['steps'][i]['html_instructions'])
					d = (result['routes'][0]['legs'][0]['steps'][i]['distance']['text'])
					l = (result['routes'][0]['legs'][0]['steps'][i]['duration']['text'])
					s = re.sub('<[A-Za-z\/][^>]*>', '', s)
					output.writelines(s + " " + d + " " + l + '\n')

			if printer is None:
				action = 'print'
			else:
				action = 'printto'
				printer = '"%s"' % printer

			for x in range(print_copies):
				ShellExecute(
					0,
					action,
					filename,
					printer,
					'.',
					0
				)

	PLUGIN = directions
