#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import canvas
from libopensesame.exceptions import osexception
import serial
import sys
import re

import marker_management as mark


class markers(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Handles communication with Leiden Univ marker devices'

	def reset(self):

		"""
		desc:
			Resets plug-in to initial values.
		"""

		self.var.marker_device = u'UsbParMar'
		self.var.marker_mode = u'Send marker'
		self.var.marker_device_addr = u'ANY'
		self.var.marker_device_serial = u'ANY'
		self.var.marker_device_tag = u'marker_device_1'
		self.var.marker_value = 0
		self.var.marker_duration = 0
		self.var.marker_reset_to_zero = 'yes'
		self.var.marker_crash_on_mark_errors = u'yes'
		self.var.marker_dummy_mode = 'yes'
		self.var.marker_gen_mark_file = u'yes'
		self.var.marker_flash_255 = u'yes'

		print(self.var.marker_duration)
		print(type(self.var.marker_duration))

	def get_device(self):
		if self.var.marker_device == u'UsbParMar':
			device = 'UsbParMar'
		elif self.var.marker_device == u'EVA':
			device = 'EVA'
		else:
			raise osexception(u'INTERNAL ERROR')
		return device

	def get_cur_mode(self):
		if self.var.marker_mode == u'Send marker':
			mode = 'send'
		elif self.var.marker_mode == u'Initialize':
			mode = 'init'
		else:
			raise osexception(u'INTERNAL ERROR')
		return mode

	def get_addr(self):
		return self.var.marker_device_addr

	def get_serial(self):
		return self.var.marker_device_serial

	def get_tag(self):
		return self.var.marker_device_tag

	def get_dummy_mode(self):
		if self.var.marker_dummy_mode == u'yes':
			dummy_mode = True
		else:
			dummy_mode = False
		return dummy_mode

	def get_crash_on_mark_error(self):
		if self.var.marker_crash_on_mark_errors == u'yes':
			crash_on_mark_error = True
		else:
			crash_on_mark_error = False
		return crash_on_mark_error
		
	def is_already_init(self):
		return hasattr(self.experiment, f"markers_{self.get_tag()}")

	def get_marker_manager(self):
		if self.is_already_init():
			return getattr(self.experiment, f"markers_{self.get_tag()}")
		else:
			return None

	def set_marker_manager(self, mark_man):
		setattr(self.experiment, f"markers_{self.get_tag()}", mark_man)

	def prepare(self):

		"""
		desc:
			Prepare phase.
		"""
		
		# Call the parent constructor.
		item.prepare(self)

		if self.get_cur_mode() == "init":
			# Do noting in prepare when in init mode.
			pass
		elif self.get_cur_mode() == "send":
			# Do noting in prepare when in send mode.
			pass
		else:
			raise osexception("Internal mode error.")

	def run(self):
		
		"""
		desc:
			Run phase.
		"""
		
		if self.get_cur_mode() == "init":

			if self.is_already_init():
				# Raise error since you cannot init twice.
				raise osexception("Marker device already initialized.")
			else:
				# Initializes device.

				# Resolve device:
				info = self.resolve_com_port()

				# Build serial manager:
				marker_manager = mark.MarkerManager(self.var.marker_device,
													device_address=info['com_port'],
													fallback_to_fake=self.get_dummy_mode(),
													crash_on_marker_errors=self.get_crash_on_mark_error(),
													time_function_us=lambda: self.time() * 1000)
				self.set_marker_manager(marker_manager)

				# Flash 255
				pulse_dur = 100
				if self.var.marker_flash_255 == 'yes':
					marker_manager.set_value(255)
					self.sleep(pulse_dur)
					marker_manager.set_value(0)
					self.sleep(pulse_dur)
					marker_manager.set_value(255)
					self.sleep(pulse_dur)

				# Reset:
				marker_manager.set_value(0)
				self.sleep(pulse_dur)

				# Register de-constructor:
				# self.experiment.cleanup_functions.append(marker_manager.set_value(0))
				# self.experiment.cleanup_functions.append(self.sleep(pulse_dur))
				# self.experiment.cleanup_functions.append(self.close())
				# if self.var.marker_gen_mark_file == u'yes':
				# 	self.experiment.cleanup_functions.append(marker_manager.save_marker_table())

		elif self.get_cur_mode() == "send":
			
			# Check if initialized:
			if not self.is_already_init():
				raise osexception("You must have a marker object in initialize mode before sending markers.")

			# Send marker:
			try:
				self.get_marker_manager().set_value(int(self.var.marker_value))
			except:
				raise osexception(f"Error sending marker: {sys.exc_info()[1]}")
		
			self.sleep(int(self.var.marker_duration))

			if self.get_cur_mode() == 'send' and self.var.marker_duration > 5 and self.var.marker_reset_to_zero == 'yes':
				# Reset to 0:
				try:
					self.get_marker_manager().set_value(int(self.var.marker_value))
				except:
					raise osexception(f"Error sending marker: {sys.exc_info()[1]}")

		self.set_item_onset()

	def close(self):

		"""
		desc:
			Closes the serial connection.
		"""

		try:
			self.get_marker_manager().close()
			print("Disconnected from marker device.")
		except:
			pass

	def resolve_com_port(self):

		# Get device type
		device_type = self.get_device()
		serialno = self.get_serial()
		addr = self.get_addr()
		dummy_mode = self.get_dummy_mode()

		# Check com address
		if addr != 'ANY' and re.match("^COM\d{1,3}", addr) == None:
			raise osexception("Incorrect marker device address address:")

		# Find device
		try:
			device_info = mark.find_device(device_type=device_type, serial_no=serialno,
										   com_port=addr, fallback_to_fake=dummy_mode)
		except:
			raise osexception(f"Marker device init error: {sys.exc_info()[1]}")

		return device_info


class qtmarkers(markers, qtautoplugin):

	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		markers.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)


	def init_edit_widget(self):

		"""
		Constructs the GUI controls. Usually, you can omit this function
		altogether, but if you want to implement more advanced functionality,
		such as controls that are grayed out under certain conditions, you need
		to implement this here.
		"""

		# First, call the parent constructor, which constructs the GUI controls
		# based on info.json.
		qtautoplugin.init_edit_widget(self)
		self.custom_interactions()


	def apply_edit_changes(self):

		"""
		desc:
			Applies the controls.
		"""

		if not qtautoplugin.apply_edit_changes(self) or self.lock:
			return False
		self.custom_interactions()

	def edit_widget(self):

		"""
		Refreshes the controls.

		Returns:
		The QWidget containing the controls
		"""

		if self.lock:
			return
		self.lock = True
		w = qtautoplugin.edit_widget(self)
		self.custom_interactions()
		self.lock = False
		return w

		
	def custom_interactions(self):

		"""
		desc:
			Activates the relevant controls for each setting.
		"""


		cur_mode = self.get_cur_mode()
		if cur_mode == "init":
			enable_init = True
		elif cur_mode == "send":
			enable_init = False

		if cur_mode == "send" and self.var.marker_duration > 5:
			enable_reset = True
		else:
			enable_reset = False

		self.marker_device_widget.setEnabled(True)
		self.marker_mode_widget.setEnabled(True)

		self.marker_device_addr_widget.setEnabled(enable_init)
		self.marker_device_serial_widget.setEnabled(enable_init)
		self.marker_device_tag_widget.setEnabled(True)

		self.marker_value_widget.setEnabled(not enable_init)
		self.marker_object_duration_widget.setEnabled(not enable_init)
		self.marker_reset_to_zero_widget.setEnabled(not enable_init)

		self.marker_crash_on_mark_errors_widget.setEnabled(enable_init)
		self.marker_dummy_mode_widget.setEnabled(enable_init)
		self.marker_gen_mark_file_widget.setEnabled(enable_init)
		self.marker_flash_255_widget.setEnabled(enable_init)
