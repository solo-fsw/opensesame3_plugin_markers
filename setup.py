#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Edited from the official example for use with the ParMarker plugin.
See https://github.com/smathot/opensesame-plugin-example
"""

from setuptools import setup

import os
import glob
from setuptools import setup

parmarker_version = '0.1.0'

print("Running setup for ParMarker version {}.".format(parmarker_version))

def files(path):
	
	# Return non-pyc files (copied from PyGaze):
	return [
		fname
		for fname in glob.glob(path) if os.path.isfile(fname)
		and not fname.endswith('.pyc')
	]


def data_files():

	# Return the target folders and their respective data files:
	return [
		("share/opensesame_plugins/parmarker_init",
			files("opensesame_plugins/parmarker_init/*"))
	]


setup(
	# Some general metadata. By convention, a plugin is named:
	# opensesame-plugin-[plugin name]
	name='opensesame-plugin-usbparmarker',
	version=parmarker_version,
	description='Plugin for controlling the UsbParMarker device.',
	author='Research Support FSW',
	author_email='labsupport@fsw.leidenuniv.nl',
	url='https://github.com/solo-fsw/opensesame_plugin_usbparmarker',
	# Classifiers used by PyPi if you upload the plugin there
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: MacOS X',
		'Environment :: Win32 (MS Windows)',
		'Environment :: X11 Applications',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
	],
	# The important bit that specifies how the plugin files should be installed,
	# so that they are found by OpenSesame. This is a bit different from normal
	# Python modules, because an OpenSesame plugin is not a (normal) Python
	# module.
	data_files=data_files()
	)
