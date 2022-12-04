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
		Shows marker tables after an experiment has finished.
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
			Shows marker tables after completion of the experiment.
		"""

		try:
			var = self.extension_manager.provide(
				'jupyter_workspace_variable',
				name='var'
			)

			# init markdown
			md = ''
			md += u'#Marker tables\n'
			md += u'time: ' + str(time.ctime()) + u'\n\n'

			summary_df = var.summary_df
			marker_df = var.marker_df
			error_df = var.error_df

			# Add summary table to md
			md = self.add_table_to_md(md, summary_df, 'Summary table')

			# # Add marker table to md
			marker_df = marker_df.round(decimals=3)
			md = self.add_table_to_md(md, marker_df, 'Marker table')

			# Add error table to md
			md = self.add_table_to_md(md, error_df, 'Error table')

			self.tabwidget.open_markdown(md, u'os-finished-success', _(u'Marker tables'))

		# AttributeErorr occurs when the tables do not exist and thus no markers were sent. In that case, do nothing.
		except AttributeError:
			pass

	def add_table_to_md(self, md, df, table_title):
		md += u'##' + table_title + u':##' + u'\n'

		ncols = len(df.columns)

		# Column headers
		md += u'| '
		for column in df:
			md += column + u' | '
		md += u'\n'

		# Header separator
		md += u'|'
		for col in range(ncols):
			md += u'---|'
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
