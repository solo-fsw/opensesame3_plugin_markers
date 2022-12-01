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
_ = translation_context(u'after_experiment', category=u'extension')


class markers_extension(base_extension):

	"""
	desc:
		Shows notifications after an experiment has finished.
	"""

	def event_end_experiment(self):

		"""
		desc:
			Handles the end of an experiment.

		arguments:
			ret_val:
				desc:	An Exception, or None if no exception occurred.
				type:	[Exception, NoneType]
		"""

		self.print_markers()

	def print_markers(self):

		"""
		desc:
			Shows a summary after successful completion of the experiment.
		"""
		var = self.extension_manager.provide(
			'jupyter_workspace_variable',
			name='var'
		)

		self.tabwidget.open_markdown('mark')

		# logfile = self._logfile
		# if logfile is None:
		# 	logfile = u'Unknown logfile'
		# md = safe_read(self.ext_resource(u'finished.md')) % {
		# 	u'time': time.ctime(),
		# 	u'logfile': logfile
		# 	}
		# if self._extra_data_files:
		# 	md += u'\n' \
		# 		+ _(u'The following extra data files where created:') + u'\n\n'
		# 	for data_file in self._extra_data_files:
		# 		md += u'- `' + data_file + u'`\n'
		# 	md += u'\n'
		# self.tabwidget.open_markdown(md, u'os-finished-success', _(u'Finished'))

