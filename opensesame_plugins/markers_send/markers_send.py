# -*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
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

import marker_management as mark


class markers_send(item):
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
        self.var.marker_device_tag = u'marker_device_1'
        self.var.marker_value = 0
        self.var.marker_object_duration = 0
        self.var.marker_reset_to_zero = 'no'

    def get_tag(self):
        return self.var.marker_device_tag

    def get_value(self):
        return self.var.marker_value

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

        if not self.is_already_init():
            raise osexception("You must have a marker object in initialize mode before sending markers."
                              "Make sure the Device tags match.")

        # Call the parent constructor.
        item.prepare(self)

    def run(self):

        """
        desc:
            Run phase.
        """

        # Send marker:
        try:
            self.get_marker_manager().set_value(int(self.var.marker_value))
        except:
            raise osexception(f"Error sending marker with value {self.var.marker_value}: {sys.exc_info()[1]}")

        # Sleep for object duration (blocking)
        self.sleep(int(self.var.marker_object_duration))

        # Reset marker value to zero, if specified:
        if self.var.marker_object_duration > 5 and self.var.marker_reset_to_zero == 'yes':

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

        # We don't need to do anything here, except call the parent
        # constructors.
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
