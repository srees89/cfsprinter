#!/usr/bin/env python
"""
Display Plugin
Copyright 2016 Shane Rees <https://github.com/Shaggs/>

A Small GUI to display pager message on a screen. Will change from
Green > orange > Red at a 3 minute interval this way upon entering the
station you can have a ruff indication of response time.

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
from Tkinter import Tk, BOTH, INSERT, Text
import re


class Display(BasePlugin):
	def configure(self, c):
		self.size = c.get('display', 'font-size')
	def execute(self, msg, unit, address, when, printer, print_copies):
		if "P1" in msg:
			msg = msg.replace(" P1 ", ", ALARM LEVEL: 1, ")
		elif "P2" in msg:
			msg = msg.replace(" P2 ", ", ALARM LEVEL: 1, ")
		elif "P3" in msg:
			msg = msg.replace(" P3 ", ", ALARM LEVEL: 1, ")
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
		if 'P1' or 'P2' or 'P3' in msg:
			tg = "null"
		else:
			tg = addr.split(',')[4]
		if "== ==" in addr:
		 ex = addr.split("== ==")[1]
		else:
		 ex = addr.split("==")[1]
		ex = ex.split(':')[0]
		sunit = msg.split (':')[6]
		ex = ex.replace('==' or "== ==", '')
		if tg == 'null':
			tg = ' '
		else:
			tg = re.sub(r'TG', '', tg)
			tg = tg.strip("  ")
		addr = addr.split(trigger_end)[0]
		addr = re.sub(r'#\d{3}/\d{3}|@|\s:\s', '', addr)
		addr_p = addr.split(',')[-2:]
		addr = ','.join(addr_p)
		def orange():
			text_widget.config(bg="Orange")
			root.after(180000, red)

		def red():
			text_widget.config(bg="Red")
			root.after(180000, kill)

		def kill():
			root.destroy()
		size = str('times ' + self.size + ' bold')
		mseg = str('%s - %s' % (msg, unit))
		root = Tk()
		text_widget = Text(root, font=size, bg='Green')
		text_widget.pack(fill=BOTH, expand=0)
		text_widget.tag_configure('tag-center', wrap='word', justify='center')
		text_widget.insert(INSERT,''' Date: %(date)s

Time: %(time)s 

Incident Type: %(inc)s  

Incident Number: %(incno)s

Level: %(alarm)s

Message: %(ex)s

Info/Address: %(addr)s

Map Ref: %(map)s

Talk Group: %(tg)s 

Resources: %(sunit)s

Raw:  %(msg)s '''
		% dict(msg=msg, incno=incno, inc=inc, alarm=alarm, addr=addr, ex=ex, tg=tg, sunit=sunit, map=map, date=date,time=time), 'tag-center')
		root.after(180000, orange)
		root.mainloop()

PLUGIN = Display















