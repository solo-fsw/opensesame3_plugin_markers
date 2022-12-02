#-*- coding:utf-8 -*-

"""
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
		Shows notifications after an experiment has finished.
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
			Shows a summary after successful completion of the experiment.
		"""

		# init markdown
		md = ''

		var = self.extension_manager.provide(
			'jupyter_workspace_variable',
			name='var'
		)

		summary_df = var.summary_df
		marker_df = var.marker_df
		error_df = var.error_df

		# Add summary table to md
		md = add_table_to_md(md, summary_df, 'Summary table')

		# # Add marker table to md
		marker_df = marker_df.round(decimals=3)
		md = add_table_to_md(md, marker_df, 'Marker table')

		# Add error table to md
		md = add_table_to_md(md, error_df, 'Error table')

		self.tabwidget.open_markdown(md, u'os-finished-success', _(u'Marker tables'))


def add_table_to_md(md, df, table_title):
	md += _(u'***' + table_title + ':***') + u'\n\n'

	ncols = len(df.columns)

	# Column headers
	md += _(u'| ')
	for column in df:
		md += column + _(u' | ')
	md += u'\n'

	# Header separator
	md += _(u'|')
	for col in range(ncols):
		md += _(u'---|')
	md += u'\n'

	# Values
	md += _(u'| ')
	for index, row in df.iterrows():
		for column in df:
			cur_value = row[column]
			if isinstance(cur_value, float):
				cur_value = round(cur_value, 3)
			md += str(cur_value) + _(u' | ')

		md += u'\n'

	md += u'\n\n'

	return md
