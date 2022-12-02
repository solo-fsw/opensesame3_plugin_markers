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

	@property
	def _summary_df(self):

		"""
		returns:
			desc:	The summary data frame of the last run, or None if this
					could not be determined.
			type:	[df, NoneType]
		"""

		# Depending on the runner, the logfile is either a property of the
		# var object ...
		var = self.extension_manager.provide(
			'jupyter_workspace_variable',
			name='var'
		)
		try:
			if var and 'summary_df' in var:
				return var.summary_df
		except TypeError:
			# JupyterConsole returns a custom FailedToGetWorkspaceVariable
			# Exception when an error occurs. This is not iterable and results
			# in a TypeError.
			pass
		# ... or it is a global variable in the workspace
		summary_df = self.extension_manager.provide(
			'jupyter_workspace_variable',
			name='summary_df'
		)
		if summary_df:
			return summary_df

	def print_markers(self):

		"""
		desc:
			Shows a summary after successful completion of the experiment.
		"""

		summary_df = self._summary_df

		if summary_df is None:
			summary_df = u'Unknown summary_df'

		md = ''
		md += u'\n' + \
			  _(u'***Summary table:***') + u'\n\n'
		md += _(u'value | occurrences') + u'\n'
		md += _(u'---|---') + u'\n'
		md += _(u'1 | 1') + u'\n'
		md += _(u'2 | 1') + u'\n'
		md += u'\n\n\n'
		self.tabwidget.open_markdown(md, u'os-finished-success', _(u'Marker tables'))

