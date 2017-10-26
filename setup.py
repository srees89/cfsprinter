#!/usr/bin/env python
from setuptools import setup
from sys import version, platform

requires = ['beautifulsoup4', 'configparser']

if platform == 'win32':
	try:
		import py2exe  # nopep8
	except ImportError:
		print "Warning: py2exe is not installed. You will not be able to build py2exe"
		print "targets without it!"

	requires.append('win32api')

if version < '2.6.0':
	requires.append("simplejson")

setup(
	name='pagerprinter',
	version='0.1.4',
	author='Michael Farrell',
	url='http://github.com/micolous/cfsprinter',
	options=dict(py2exe=dict(includes=[
		'pagerprinter.plugins.winprint',
		'pagerprinter.plugins.lpdprint',
		'pagerprinter.plugins.skypesms',
		'pagerprinter.plugins.logfile',
		'pagerprinter.plugins.huaweisms',
		'pagerprinter.plugins.email',
		'pagerprinter.plugins.__init__',
		'pagerprinter.plugins.display',
		'pagerprinter.plugins.tts',
		'pagerprinter.plugins.directions',
	])),

	requires=requires,
	license='GPL3',
	console=[
		dict(script='py2exe_run.py', icon_resources=[(0, "pager.ico")]),
	],

	data_files=[('doc/pagerprinter', [
		'pagerprinter.example.ini',
		'README.md',
		'LICENSE.txt',
	])],

	package_dir={'pagerprinter': 'src/pagerprinter'},
	packages=[
		'src',
		'pagerprinter',
		'pagerprinter.misc',
		'pagerprinter.plugins',
		'pagerprinter.scrapers',
	],
	entry_points={
		'console_scripts': [
			'pagerprinter = pagerprinter.pagerprinter:main',
		]
	}
)
