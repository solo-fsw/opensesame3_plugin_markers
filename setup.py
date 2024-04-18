#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Edited from the official example for markers plugin.
See https://github.com/smathot/opensesame-plugin-example
"""

from setuptools import setup
import os
import glob
import version_info

print("Running setup for markers_os3 version {}.".format(version_info.version))

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
		("share/opensesame_plugins/markers_os3_send",
		 files("opensesame_plugins/markers_os3_send/*")),
		("share/opensesame_plugins/markers_os3_init",
		 files("opensesame_plugins/markers_os3_init/*")),
		("share/opensesame_extensions/markers_os3_extension",
		 files("opensesame_extensions/markers_os3_extension/*")),
		 ("share/opensesame_plugins/markers_os3_init", 
    	["version_info.py"]),
		 ("share/opensesame_plugins/markers_os3_send", 
    	["version_info.py"])	    
	]


setup(
	# Some general metadata. By convention, a plugin is named:
	# opensesame-plugin-[plugin name]
	name=version_info.name,
	version=version_info.version,
	description=version_info.description,
	author=version_info.author,
	author_email=version_info.author_email,
	url=version_info.url,
	install_requires=version_info.install_requires,
	# The important bit that specifies how the plugin files should be installed,
	# so that they are found by OpenSesame. This is a bit different from normal
	# Python modules, because an OpenSesame plugin is not a (normal) Python
	# module.
	data_files=data_files()
	)
