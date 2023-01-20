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

markers_version = '0.1.0'

print("Running setup for markers version {}.".format(markers_version))

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
		("share/opensesame_plugins/markers_send",
		 files("opensesame_plugins/markers_send/*")),
		("share/opensesame_plugins/markers_init",
		 files("opensesame_plugins/markers_init/*")),
		("share/opensesame_plugins/markers_send/utils",
		 files("opensesame_plugins/markers_send/utils/*")),
		("share/opensesame_plugins/markers_init/utils",
		 files("opensesame_plugins/markers_init/utils/*")),
		("share/opensesame_extensions/markers_extension",
		 files("opensesame_extensions/markers_extension/*"))
	]


setup(
	# Some general metadata. By convention, a plugin is named:
	# opensesame-plugin-[plugin name]
	name='opensesame-plugin-markers',
	version=markers_version,
	description='Plugin for controlling Leiden Univ marker devices.',
	author='SOLO Research Support FSW Leiden',
	author_email='labsupport@fsw.leidenuniv.nl',
	url='https://github.com/solo-fsw/opensesame_plugin_markers',
	# Classifiers used by PyPi if you upload the plugin there
	classifiers=[
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering',
		'Environment :: Win32 (MS Windows)',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 3'],
	# The important bit that specifies how the plugin files should be installed,
	# so that they are found by OpenSesame. This is a bit different from normal
	# Python modules, because an OpenSesame plugin is not a (normal) Python
	# module.
	data_files=data_files()
	)
