#-*- coding:utf-8 -*-

"""
OpenSesame extension for creating a tab with the marker tables after the experiment is finished.
"""

import time
import os
import json
from libopensesame.py3compat import *
from libopensesame.exceptions import osexception
from libqtopensesame.extensions import base_extension
from libopensesame import misc
from libqtopensesame.misc.translate import translation_context
import markdown
import pandas


class markers_extension(base_extension):

	"""
	desc:
		Shows marker tables in separate tab after an experiment has finished.
	"""

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

				# Add marker table to md
				marker_df = marker_df.round(decimals=3)
				md = add_table_to_md(md, marker_df, 'Marker table')

				# Add error table to md
				md = add_table_to_md(md, error_df, 'Error table')

			# Open the tab
			self.tabwidget.open_markdown(md, u'os-finished-success', u'Marker tables')

		# AttributeErorr occurs when the tables do not exist and thus no markers were sent. In that case, do nothing.
		except AttributeError:
			pass


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
