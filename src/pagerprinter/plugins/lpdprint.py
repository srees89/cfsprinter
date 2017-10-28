#!/usr/bin/env python
"""
LPD/CUPS text printing plugin for pagerprinter.
Copyright 2011 - 2015 Michael Farrell <http://micolous.id.au/>

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
import re


class LPDPrintPlugin(BasePlugin):
	"""\
This plugin prints out a text document using LPD/CUPS of the details, using the
lpr command.
"""
	def configure(self, c):
		try:
			self.cpi = c.getint('pagerprinter', 'print-cpi')
		except NoOptionError:
			self.cpi = None

		try:
			self.lpi = c.getint('pagerprinter', 'print-lpi')
		except NoOptionError:
			self.lpi = None

	def execute(self, msg, unit, address, when, printer, print_copies):
		trigger = 'RESPOND'
		trigger_end = 'MAP'
		addr = msg.split(trigger)[1]
		incno = msg.split(' ')[2]
		date = msg.split(' ')[3]
		time = msg.split(' ')[4]
		inc = addr.split(',')[0]
		alarm = addr.split(',')[1]
		map = addr.split(',')[3]
		map = re.sub(r'MAP:', '', map)
		tg = addr.split(',')[4]
		if "== ==" in addr:
		 ex = addr.split("== ==")[1]
		else:
		 ex = addr.split("==")[1]
		ex = ex.split(':')[0]
		sunit = msg.split (':')[6]
		ex = ex.replace('==' or "== ==", '')
		tg = re.sub(r'TG', '', tg)
		tg = tg.strip("  ")
		addr = addr.split(trigger_end)[0]
		addr = re.sub(r'#\d{3}/\d{3}|@|\s:\s', '', addr)
		addr_p = addr.split(',')[-2:]
		addr = ','.join(addr_p)
		
		pargs = ['lpr', '-#', str(print_copies)]

		if printer is not None:
			pargs += ['-P', printer]

		if self.cpi is not None:
			pargs += ['-o', 'cpi=%d' % self.cpi]

		if self.lpi is not None:
			pargs += ['-o', 'lpi=%d' % self.lpi]

		for x in range(print_copies):
			lpr = subprocess.Popen(pargs, stdin=subprocess.PIPE)

			lpr.stdin.write("""\
Date: %(date)s			Time: %(time)s 

Incident Type: %(inc)s

Incident Number: %(incno)s

Level: %(alarm)s

Message: %(ex)s

Info/Address: %(addr)s

Map Ref: %(map)s

Talk Group: %(tg)s 

Resources: %(sunit)s

Raw:  %(msg)s """
		% dict(msg=msg, incno=incno, inc=inc, alarm=alarm, addr=addr, ex=ex, tg=tg, sunit=sunit, map=map, date=date,time=time))
		

			lpr.stdin.flush()
			lpr.stdin.close()

PLUGIN = LPDPrintPlugin
