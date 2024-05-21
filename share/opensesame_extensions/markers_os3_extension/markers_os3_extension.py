#-*- coding:utf-8 -*-

"""
OpenSesame extension for creating a tab with the marker tables after the experiment is finished.
Part of the markers_os3 plugin.
"""

import time
from libopensesame.py3compat import *
from libqtopensesame.extensions import base_extension
from libopensesame.plugins import list_plugins, plugin_disabled
from libopensesame.metadata import major_version
from libqtopensesame.misc.config import cfg
import sys


class markers_os3_extension(base_extension):

	"""
	desc:
		- Checks OpenSesame version on startup.
		- Shows marker tables in separate tab after an experiment has finished.
	"""

	def event_startup(self):

		"""
		desc:
			Handles startup of OpenSesame
		"""		

		self.check_version()


	def event_open_experiment(self, path):

		"""
		desc:
			Handles open experiment
		"""	

		self.check_version()
		

	def check_version(self):		

		md = ''	

		if major_version[0] == '3':

			list_wrong_plugins = ["markers_os4_extension", "markers_os4_init", "markers_os4_send", "markers_extension", "markers_init", "markers_send"]
			plugins_available = []

			# Get list of plugins and extensions
			plugin_list = list_plugins(filter_disabled=True)
			extension_list = list_plugins(filter_disabled=True, _type=u'extensions')

			# Loop through lists and check whether old plugins/extensions are installed
			for plugin_name in plugin_list:
				if plugin_name in list_wrong_plugins:
					cfg_key = f'plugin_enabled_{plugin_name}'
					# Ignore disabled plugins
					if cfg_key in cfg and not cfg[cfg_key]:
						continue
					plugins_available.append(plugin_name)

			for extension_name in extension_list:
				if extension_name in list_wrong_plugins:
					cfg_key = f'plugin_enabled_{extension_name}'
					# Ignore disabled extension
					if cfg_key in cfg and not cfg[cfg_key]:
						continue
					plugins_available.append(extension_name)

			if plugins_available:
				self.extension_manager.fire(u'notify',
					message=_(u'One or more marker plugins with incompatible versions were found. Check the markers plugin warning tab for more info.'),
					category=u'warning')
				
				md += '**Warning:** The following marker plugins/extensions were found: \n\n'
				for plugin in plugins_available:
					md += '- ' + str(plugin) + '\n\n'

				md += '''These plugins/extensions should not be used in OpenSesame 3. 
						It is advised to disable them in Tools > Plug-in and extension manager.'''

				self.tabwidget.open_markdown(md, title=_(u'Markers plugin warning'), icon=u'document-new')

		else:

			self.extension_manager.fire(u'notify',
				message=_(u'The markers_os3 plugin can only run in OpenSesame 3. Check the markers plugin warning tab for more info.'),
				category=u'warning')
			
			md += '**Warning:** The markers_os3 plugin has been installed, but will not work in the current version of OpenSesame.\n\n'
			md += 'This plugin contains the following elements:\n\n'
			md += '- markers_os3_extension\n\n'
			md += '- markers_os3_init\n\n'
			md += '- markers_os3_send\n\n'
			md += 'It is advised to disable the plugins/extensions as listed above in Tools > Plug-in and extension manager.\n\n'
			md += '''When using OpenSesame 4 and you want to send markers with a Leiden Univ marker device, 
					please install the markers_os4 plugin: 
					[https://github.com/solo-fsw/opensesame4_plugin_markers](https://github.com/solo-fsw/opensesame4_plugin_markers).'''
		
			self.tabwidget.open_markdown(md, title=_(u'Markers plugin warning'), icon=u'document-new')


	def event_end_experiment(self, ret_val):

		"""
		desc:
			Handles the end of an experiment.

		arguments:
			ret_val:
				desc:	An Exception, or None if no exception occurred.
				type:	[Exception, NoneType]
		"""

		if ret_val is None:
			self.print_markers()
		else:
			self.print_markers()

	def print_markers(self):

		"""
		desc:
			Prints marker tables in md file that is shown in tab after the experiment.
		"""

		try:
			var = self.extension_manager.provide(
				'jupyter_workspace_variable',
				name='var'
			)

			if hasattr(var, 'markers_tags'):

				# Get tag(s) of marker device(s)
				marker_tags = var.markers_tags

				# Init markdown, print basic header info
				md = ''
				md += u'Time: ' + str(time.ctime()) + u'\n\n'

				# Append marker tables of each marker device:
				for tag in marker_tags:

					# Print marker device properties
					md += u'#' + str(tag) + u'\n'
					cur_marker_props = getattr(var, f"markers_prop_{tag}")

					for marker_prop in cur_marker_props:
						md += u'- ' + str(marker_prop) + u': ' + str(cur_marker_props[marker_prop]) + u'\n'

					# Get marker tables
					marker_df = getattr(var, f"markers_marker_table_{tag}")
					summary_df = getattr(var, f"markers_summary_table_{tag}")
					error_df = getattr(var, f"markers_error_table_{tag}")

					# Add summary table to md
					summary_df = summary_df.round(decimals=3)
					md = add_table_to_md(md, summary_df, 'Summary table')

					if summary_df.empty:
						md += u'No markers were sent, summary table empty\n\n'

					# Add marker table to md
					marker_df = marker_df.round(decimals=3)
					md = add_table_to_md(md, marker_df, 'Marker table')

					if marker_df.empty:
						md += u'No markers were sent, marker table empty\n\n'

					# Add error table to md
					md = add_table_to_md(md, error_df, 'Error table')

					if error_df.empty:
						md += u'No marker errors occurred, error table empty\n\n'

				# Open the tab
				self.tabwidget.open_markdown(md, u'os-finished-success', u'Marker tables')

		# Occasionally, something goes wrong getting the marker tables
		except:

			md += f'\n\nError: {sys.exc_info()[1]}'
			md += u'\n\nSomething went wrong while generating the marker tables. This can happen when the experiment is aborted or the experiment crashed.'
			self.tabwidget.open_markdown(md, u'os-finished-user-interrupt', u'Marker tables')
			

def add_table_to_md(md, df, table_title):

	# Table title
	md += u'##' + table_title + u':##' + u'\n'

	ncols = len(df.columns)

	# Column headers
	md += u'| '
	for column in df:

		if "_s" in column:
			column = column.replace("_s", " (s)")
		if "_ms" in column:
			column = column.replace("_ms", " (ms)")
		if "_" in column:
			column = column.replace("_", " ")
		column = column.capitalize()

		md += column + u' | '
	md += u'\n'

	# Header separator
	md += u'|'
	for col in range(ncols):
		md += u':---|'
	md += u'\n'

	# Values
	md += u'| '
	for index, row in df.iterrows():
		for column in df:
			cur_value = row[column]
			if isinstance(cur_value, float):
				cur_value = round(cur_value, 3)
			md += str(cur_value) + u' | '
		md += u'\n'

	md += u'\n\n'

	return md
