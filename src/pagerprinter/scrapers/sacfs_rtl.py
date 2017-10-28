#!/usr/bin/env python
from __future__ import absolute_import
import asyncore
from datetime import datetime 
from .sacfs_flexcode import CODES
import subprocess, sys
from clint.textui import puts, colored
import time, psutil

__all__ = [
    'CFSRTLScraper',
]


class CFSRTLScraper(object):
 def __init__(self, handler):
   self.feed_handler = None
   print "hello2"
 def kill():
  for process in psutil.process_iter():
   l = str(process)
   l = l.split(',')[1]
   if "name='rtl_fm'" in l:
    print "process found: " + l
    print "killing now"
    print l
   else:
    pass
        # Update frequency is not relevant
 def process_message(self):
	time = datetime.now().strftime('%H:%M:%S')
	when = datetime.now().strftime('%d/%m/%Y %H:%M')
	comm = "rtl_fm -A lut -s 22050 -f 148.8125M - | multimon-ng -t raw -a FLEX -f alpha /dev/stdin"
	multimon_ng = subprocess.Popen("rtl_fm -o 4 -A lut -s 22050 -f 148.8125M - | multimon-ng -t raw -a FLEX -f alpha /dev/stdin", 
stdout=subprocess.PIPE,
		shell=True)
	while 1:	
		try:
			when = datetime.now().strftime('%d/%m/%Y %H:%M')
   	 		decoded = str(multimon_ng.stdout.readline())
   			flex, mdate, mtime, bitrate, other, capcode, o2, msg = decoded.split(" ",7)
   	 		capcode = str(capcode)
			flexcode = capcode.replace("]", " ")
			flexcode = flexcode.replace("[", " ")
   			flexcode = int(flexcode)
   			if flexcode not in CODES:
    				flexcode = capcode
   			else: 
    				flexcode = str(CODES[flexcode])    
   			puts(" [", newline=False)
   			puts(colored.green(when), newline=False)
   			puts("] ", newline=False)
   			if "CFSRES" in msg:
    				puts(colored.red(msg + " "), newline=False)
   			else:
    				puts(msg + " ", newline=False)
   			puts(colored.yellow(flexcode))
			self.handler(
                           good_parse=True,
                           date=when,
                           unit=CODES[flexcode],
                           msg=msg)
                        print unit + " " + good_parse
			multimon_ng.poll()	
		except Exception as a:
   			print a
		sys.stdout.flush()
 def handler(self, **kwargs):
		self.feed_handler(**kwargs)

 def update(self, feed_handler):
		"""
		Pings feed for new events.
		"""
		self.feed_handler = feed_handler

 def update_forever(self, feed_handler):
		self.update(feed_handler)
		self.process_message()


