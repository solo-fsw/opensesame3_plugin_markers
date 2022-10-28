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

import serial_lib

# Connection parameters for the ParMarker in data mode:
parmarker_data_params = { "baudrate": 115200, "bytesize": 8
                                , "parity": 'N', "stopbits": 1
                                , "timeout": 2}





class parmarker_init(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Initializes a USB ParMarker device. This item can only be used once.'


	def reset(self):

		"""
		desc:
			Resets plug-in to initial values.
		"""


		self.var.mode           = u'Send marker'
		self.var.parmarker_addr = u'ANY'
		self.var.parmarker_tag  = u'ParMarker'
		self.var.marker_value   = 0
		self.var.object_duration = 0

		self.var.flash_255           = u'yes'
		self.var.throw_error_on_repeat           = u'yes'
		self.var.throw_error_on_too_short_marker = u'yes'
		self.var.throw_soft_errors               = u'no'


	def get_cur_mode(self):
		if self.var.mode == u'Send marker':
			mode = 'send'
		elif self.var.mode == u'Initialize ParMarker':
			mode = 'init'
		else:
			raise osexception(u'INTERNAL ERROR')
		return mode


	
	def get_tag(self):
		return self.var.parmarker_tag
		
	def is_already_init(self):
		return hasattr(self.experiment, f"parmarker_serial_{self.get_tag()}")

	def get_serial_manager(self):
		if self.is_already_init():
			return getattr(self.experiment, f"parmarker_serial_{self.get_tag()}")
		else:
			return None

	def set_serial_manager(self, ser_man):
		setattr(self.experiment, f"parmarker_serial_{self.get_tag()}", ser_man)

	
	def prepare(self):

		"""
		desc:
			Prepare.
		"""
		
		# Call the parent constructor.
		item.prepare(self)

		if self.get_cur_mode() == "init":
			if self.is_already_init():
				# Raise error since you cannot init twice.
				pass
			else:
				# Initializes device.

				# Resolve device:
				info = self.resolve_com_port()

				# Build serial manager:
				serial_manager = serial_lib.Serial_Manager(com_port=info['com_port'])
				self.set_serial_manager(serial_manager)

				pulse_dur = 100
				if self.var.flash_255 == 'yes':
					serial_manager.send(255)
					self.sleep(pulse_dur)
					serial_manager.send(0)
					self.sleep(pulse_dur)
					serial_manager.send(255)
					self.sleep(pulse_dur)

				# Reset:
				serial_manager.send(0)
				self.sleep(pulse_dur)

				
				# Register de-constructor:
				self.experiment.cleanup_functions.append(self.close)

		elif self.get_cur_mode() == "send":
			# Do noting in prepare when in send mode.
			pass
		else:
			raise osexception("Internal mode error.")


	def run(self):
		
		"""
		desc:
			Sets up and opens the serial device.
		"""
		
		if self.get_cur_mode() == "init":
			# Do nothing in run in init mode.
			pass
		elif self.get_cur_mode() == "send":
			
			# Check if initialized:
			if not self.is_already_init():
				raise osexception("You must have a ParMarker object in initialize mode before sending markers.")

			# Send marker:
			try:
				self.get_serial_manager().send(int(self.var.marker_value))

			except:
				raise osexception(f"Error sending marker: {sys.exc_info()[1]}")
		
		self.sleep(int(self.var.marker_value))
		self.set_item_onset()


	def close(self):

		"""
		desc:
			Closes the serial connection.
		"""

		try:
			self.experiment.parmarker_serial.close()
			print("Disconnected from ParMarker device.")
		except:
			pass



	def resolve_com_port(self):

		# Resolve the port to use:
		if self.var.parmarker_addr == "ANY":
			port_regexp = "^.*$"
		elif self.var.parmarker_addr == 'FAKE':
			port_regexp = serial_lib.Serial_Manager.FAKE_COM_ADDR
		elif re.match("^COM\d{1,3}", self.var.parmarker_addr) != None:
			port_regexp = "^" + self.var.parmarker_addr + "$"
		else:
			raise osexception("Incorrect ParMarker address:")
		
		# Find device:
		try:
			com_filters = serial_lib.gen_com_filters(port_regex = port_regexp)
			info = serial_lib.find_device(com_filters)
		except:
			raise osexception(f"ParMarker init error: {sys.exc_info()[1]}")

		return info
	





class qtparmarker_init(parmarker_init, qtautoplugin):

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
		parmarker_init.__init__(self, name, experiment, script)
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
			Activates the relevant controls for each tracker.
		"""


		cur_mode = self.get_cur_mode()
		if cur_mode == "init":

			enableIt = True

		elif cur_mode == "send":

			enableIt = False

			
		self.parmarker_addr_widget.setEnabled(enableIt)
		self.parmarker_tag_widget.setEnabled(enableIt)

		self.marker_value_widget.setEnabled(not enableIt)
		self.object_duration_widget.setEnabled(not enableIt)

		self.flash_255_widget.setEnabled(enableIt)
		self.throw_error_on_repeat_widget.setEnabled(enableIt)
		self.throw_error_on_too_short_marker_widget.setEnabled(enableIt)
		self.throw_soft_errors_widget.setEnabled(enableIt)






