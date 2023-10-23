# -*- coding:utf-8 -*-

"""
OpenSesame plugin for sending markers to Leiden Univ Marker device.
"""

from libopensesame.py3compat import *
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception
import serial
import sys
import re
import os
import pandas


class markers_send(item):
    """
    This class handles the basic functionality of the item.
    """

    description = 'Sends marker to Leiden Univ marker device - Markers plugin for OpenSesame 3'

    def reset(self):

        """
        desc:
            Resets plug-in to initial values.
        """
        self.var.marker_device_tag = u'marker_device_1'
        self.var.marker_value = 0
        self.var.marker_object_duration = 0
        self.var.marker_reset_to_zero = 'no'

    def get_tag(self):
        return self.var.marker_device_tag

    def get_value(self):
        return self.var.marker_value
    
    def get_duration(self):
        return self.var.marker_object_duration
    
    def get_reset_to_zero(self):
        return self.var.marker_reset_to_zero == u'yes'    

    def is_already_init(self):
        try:
            return hasattr(self.experiment, f"markers_{self.get_tag()}")
        except:
            return False

    def get_marker_manager(self):
        if self.is_already_init():
            return getattr(self.experiment, f"markers_{self.get_tag()}")
        else:
            return None

    def prepare(self):

        """
        desc:
            Prepare phase.
        """

        # Check input of plugin:
        device_tag = self.get_tag()
        if not(bool(re.match("^[A-Za-z0-9_-]*$", device_tag)) and bool(re.match("^[A-Za-z]*$", device_tag[0]))):
            # Raise error, tag can only contain: letters, numbers, underscores and dashes and should start with letter.
            raise osexception("Device tag can only contain letters, numbers, underscores and dashes "
                              "and should start with a letter.")
        
        # Marker value is checked by marker_management

        # Check Marker duration
        if not(isinstance(self.get_duration(), int) and not(isinstance(self.get_duration(), float))):
            raise osexception("Object duration should be numeric")
        elif self.get_duration() < 0:
            raise osexception("Object duration must be a positive number")

        # Call the parent constructor.
        item.prepare(self)

    def run(self):

        """
        desc:
            Run phase.
        """

        # Check if the marker device is initialized
        if not self.is_already_init():
            raise osexception("You must have a markers_init item before sending markers."
                              " Make sure the Device tags match.")

        # Send marker:
        try:
            self.get_marker_manager().set_value(int(self.get_value()))
        except:
            raise osexception(f"Error sending marker with value {self.get_value()}: {sys.exc_info()[1]}")

        # Sleep for object duration (blocking)
        self.sleep(int(self.get_duration()))

        # Reset marker value to zero, if specified
        if self.get_duration() > 5 and self.get_reset_to_zero():

            try:
                self.get_marker_manager().set_value(0)
            except:
                raise osexception(f"Error sending marker with value 0: {sys.exc_info()[1]}")

        self.set_item_onset()
        

class qtmarkers_send(markers_send, qtautoplugin):
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

        # Call the parent constructors.
        markers_send.__init__(self, name, experiment, script)
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
        