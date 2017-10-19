#!/usr/bin/env python
"""
Pushover Plugin

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
import requests


class PushoverPlugin(BasePlugin):
	def configure(self, c):
		self.recipient = [
			x.strip()
			for x
			in c.get('pushover', 'to').lower().split(',')
		]

		self.token = c.get('pushover', 'api')
		self.retry = c.get('pushover', 'retry')
		self.expire = c.get('pushover', 'expire')

	def execute(self, msg, unit, address, when, printer, print_copies):
	 	 params = {
            'token': token,
            'user': to,
            'title': unit,
            'message': msg,
            'priority': 2,
            'retry': retry,
            'expire': expire,
            'sound': 'updown',
        }
        requests.post('https://api.pushover.net/1/messages.json', data=params)
        print "page sent to: " + to 

PLUGIN = PushoverPlugin
