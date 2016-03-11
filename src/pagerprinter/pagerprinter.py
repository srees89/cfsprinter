#!/usr/bin/env python
"""
Program to automatically print out CFS pager feeds.
Copyright 2010 - 2015 Michael Farrell <http://micolous.id.au/>

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

from .scrapers import get_scraper
from .plugins import get_plugin
# configparser3
from configparser import SafeConfigParser, NoOptionError
from argparse import ArgumentParser, FileType
import re
import time

def run(fh=None):
	print """\
pagerprinter v0.1.3+
Copyright 2010 - 2016 Michael Farrell <http://micolous.id.au/> Shane Rees <https://github.com/>
"""
	# parse config
	c = SafeConfigParser()
	c.read_dict({
		'pagerprinter': {
			'update-freq': '30',
			'backend': 'sacfs',
			'browser-wait': '20',
			'trigger': 'RESPOND',
			'trigger-end': 'MAP',
			'print-copies': '1',
			'unit': 'all',
			'home': '141 King William Street, Adelaide SA 5000',
		},
	})

	if fh is not None:
		c.readfp(fh)

	# get a scraper instance
	scraper = get_scraper(
		c.get('pagerprinter', 'backend')
	)(
		c.getint('pagerprinter', 'update-freq')
	)
	trigger = c.get('pagerprinter', 'trigger').lower().strip()
	trigger_end = c.get('pagerprinter', 'trigger-end').lower().strip()
	my_unit = c.get('pagerprinter', 'unit').lower().strip()

	try:
		printer = c.get('pagerprinter', 'printer')
	except NoOptionError:
		printer = None
	print_copies = c.getint('pagerprinter', 'print-copies')
	if print_copies < 1:
		print "ERROR: print-copies is set to less than one.  You probably don't want this."
		return

	plugins = []
	if c.has_option('pagerprinter', 'plugins'):
		plugins = [
			get_plugin(x.strip())
			for x
			in c.get('pagerprinter', 'plugins').lower().split(',')
		]

		for plugin in plugins:
			plugin.configure(c)

	# special case: all units.
	# may result in dupe printouts
	if my_unit == 'all':
		my_unit = ''

	# now, lets setup a handler for these events.
	def page_handler(good_parse, msg, date=None, unit=None):
		if good_parse:
			# filter for unit
			if my_unit in unit.lower():
				# this is for me!!!
				print "- This is a message for my unit!"
				print "%s " % (repr(msg))
				# check for trigger
				lmsg = msg.lower()
				if trigger in lmsg:
					# trigger found
					# split by trigger and find address nicely.
					addr = lmsg.split(trigger)[1]

					if trigger_end in lmsg:
						addr = addr.split(trigger_end)[0]

						# Remove the @ symbols in the message, and the ASE device number (#nnn/nnn)
						addr = re.sub(r'#\d{3}/\d{3}|@|\s:\s', '', addr)

						# now split that up into parts, discarding the first
						# which is a description of the event
						addr_p = addr.split(',')[-2:]

						# clone the list for iteration as we well modify in this operation as well
						for i, part in enumerate(list(addr_p)):
							if 'alarm level' in part:
								del addr_p[i]
								break

						# reassemble the address
						addr = ','.join(addr_p)
						del addr_p
						print "- Address: %s" % addr

						# now, send to plugins
						for plugin in plugins:
							try:
								plugin.execute(msg, unit, addr, date, printer, print_copies)
							except Exception, e:
								print "Exception caught in plugin %s" % type(plugin)
								print e
								f = open("syslog.log", "a")
								j = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
								m = str(j)
								f.write('\n' + m)
								f.write(" Exception caught in plugin %s" % type(plugin))
								v = str(e)
								f.write(v)
								f.close()
								
						print "**** Back to Motoring***"		
					else:
						print "- WARNING: End trigger not found! You wont receive any output because of this"
				else:
					print "- Trigger not found.  Skipping..."
		else:
			print "ERROR: THIS IS A BUG!!!"
			print "Couldn't handle the following message, please file a bug report."
			print repr(msg)
	f = open("syslog.txt", "a")
	f.write("\n %s Program Started % (time.strftime("%H:%M:%S")))
	f.close()
	print "%s ***Starting***" % (time.strftime("%H:%M:%S"))
	scraper.update_forever(page_handler)


def main():
	parser = ArgumentParser()

	parser.add_argument(
		'--config', '-c', type=FileType('rb'),
		help='Configuration file to use'
	)

	options = parser.parse_args()
	run(options.config)


if __name__ == '__main__':
	main()

