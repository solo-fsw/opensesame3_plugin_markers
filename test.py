"""
Edited from the official example for use with the ParMarker plugin.
See https://github.com/smathot/opensesame-plugin-example
"""

from setuptools import setup
import os
import glob
import version_info

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
		("share/opensesame_extensions/markers_extension",
		 files("opensesame_extensions/markers_extension/*")),
		 ("share/opensesame_plugins/markers_init", 
    	["version_info.py"])

	]

data_files2 = data_files()
print(data_files2)

