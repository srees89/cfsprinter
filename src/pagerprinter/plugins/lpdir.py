#!/usr/bin/env python
"""
LPD/CUPS text printing plugin for pagerprinter.
Copyright 2011- 2015 Michael Farrell <http://micolous.id.au/>

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
import subprocess
from configparser import NoOptionError
import json, urllib, re
from urllib import urlencode


class lpdir(BasePlugin):
		def configure(self, c):
			self.home = c.get('pagerprinter', 'home')
			try:
				self.cpi = c.getint('pagerprinter', 'print-cpi')
			except NoOptionError:
				self.cpi = None
			try:
				self.lpi = c.getint('pagerprinter', 'print-lpi')
			except NoOptionError:
				self.lpi = None

		def execute(self, msg, unit, address, when, printer, print_copies):
			url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((
				('origin', self.home),
				('destination', address)
			))
			ur = urllib.urlopen(url)
			result = json.load(ur)
			for i in range(0, len(result['routes'][0]['legs'][0]['steps'])):
				s = (result['routes'][0]['legs'][0]['steps'][i]['html_instructions'])
				d = (result['routes'][0]['legs'][0]['steps'][i]['distance']['text'])
				l = (result['routes'][0]['legs'][0]['steps'][i]['duration']['text'])
				s = re.sub('<[A-Za-z\/][^>]*>', '', s)
			pargs = ['lpr', '-#', str(print_copies)]

			if printer is not None:
				pargs += ['-P', printer]

			if self.cpi is not None:
				pargs += ['-o', 'cpi=%d' % self.cpi]

			if self.lpi is not None:
				pargs += ['-o', 'lpi=%d' % self.lpi]

			for x in range(print_copies):
				lpr = subprocess.Popen(pargs, stdin=subprocess.PIPE)

				lpr.stdin.writes(s + " " + d + " " + l + '\n')

				lpr.stdin.flush()
				lpr.stdin.close()

PLUGIN = lpdir
