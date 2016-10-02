#!/usr/bin/env python
"""
Windows text printing plugin for pagerprinter.
Copyright 2011 - 2016 Michael Farrell <http://micolous.id.au/>

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
import re
from prettytable import PrettyTable
try:
	from win32api import ShellExecute
except ImportError, ex:
	print_exc()
	print "NOTICE: winprint could not be loaded on this platform."
	PLUGIN = None
else:
	from tempfile import mktemp
	class WinPrintPlugin(BasePlugin):
		"""This plugin prints out a text document on Windows of the details."""
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
			
			print "- incno: %s" % incno
			print "- date: %s" % date
			print "- time: %s" % time
			print "- inc: %s" % inc
			print "- alarm: %s" % alarm
			print "- Address: %s" % addr
			print "- map: %s" % map
			print "- tg: %s" % tg
			print "- ex: %s" % ex
			print "- unit: %s" % sunit
			filename = 'pager message.txt'
			out = open (filename, 'w').write("""
Date: %(date)s

Time: %(time)s 

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
			

	PLUGIN = WinPrintPlugin