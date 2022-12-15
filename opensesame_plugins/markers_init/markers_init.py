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


class markers_init(item):
    """
    This class (the class with the same name as the module) handles the basic
    functionality of the item. It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Handles communication with Leiden Univ marker devices'

    version = 0.1

    def reset(self):
        """
        desc:
            Resets plug-in to initial values.
        """
        self.var.marker_device_tag = u'marker_device_1'
        self.var.marker_device = u'ANY'
        self.var.marker_device_addr = u'ANY'
        self.var.marker_device_serial = u'ANY'

        self.var.marker_crash_on_mark_errors = u'yes'
        self.var.marker_dummy_mode = u'no'
        self.var.marker_gen_mark_file = u'yes'
        self.var.marker_flash_255 = u'no'

    def get_device(self):
        if self.var.marker_device == u'UsbParMarker':
            device = 'UsbParMarker'
        elif self.var.marker_device == u'Eva':
            device = 'Eva'
        elif self.var.marker_device == u'ANY':
            device = 'ANY'
        else:
            raise osexception(u'INTERNAL ERROR')
        return device

    def get_addr(self):
        return self.var.marker_device_addr

    def get_serial(self):
        return self.var.marker_device_serial

    def get_tag(self):
        return self.var.marker_device_tag

    def get_dummy_mode(self):
        return self.var.marker_dummy_mode == u'yes'

    def get_crash_on_mark_error(self):
        return self.var.marker_crash_on_mark_errors == u'yes'

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

    def set_marker_manager(self, mark_man):
        setattr(self.experiment, f"markers_{self.get_tag()}", mark_man)

    def set_marker_manager_tag(self):
        try:
            self.experiment.var.mark_man_tags.append(self.get_tag())
        except:
            try:
                setattr(self.experiment.var, "mark_man_tags", [self.get_tag()])
            except:
                pass

    def get_marker_manager_tag(self):
        if self.is_already_init():
            return getattr(self.experiment, f"mark_man_tags")
        else:
            return None

    def set_marker_vars(self, marker_vars):
        setattr(self.experiment, f"marker_vars_{self.get_tag()}", marker_vars)

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

        device_address = self.get_addr()
        if device_address != u'ANY' and re.match("^COM\d{1,3}", device_address) is None:
            # Raise error when marker address is not a proper COM address.
            raise osexception("Incorrect marker device address address:")

        if self.is_already_init():
            # Raise error since you cannot init twice.
            raise osexception("Marker device already initialized.")

        # Call the parent constructor.
        item.prepare(self)

    def run(self):

        """
        desc:
            Run phase.
        """

        # Set Fake device in dummy mode
        if self.get_dummy_mode():
            com_port = 'FAKE'
            device = 'FAKE DEVICE'
        else:
            # Resolve device:
            info = self.resolve_com_port()
            device = info['device']['Device']
            com_port = info['com_port']

        # Build serial manager:
        marker_manager = mark.MarkerManager(device_type=device,
                                            device_address=com_port,
                                            crash_on_marker_errors=self.get_crash_on_mark_error(),
                                            time_function_ms=lambda: self.time())
        self.set_marker_manager(marker_manager)

        # Add tag to marker manager tag list:
        self.set_marker_manager_tag()

        # Create marker_vars (dict with marker manager variables)
        marker_vars = marker_manager.device_properties
        marker_vars["Address"] = marker_manager.device_address
        self.set_marker_vars(marker_vars)

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

        # Add cleanup function:
        self.experiment.cleanup_functions.append(self.cleanup)

        self.set_item_onset()

    def cleanup(self):

        # Reset value:
        self.get_marker_manager().set_value(0)
        self.sleep(100)

        # Generate and save marker file
        if self.var.marker_gen_mark_file == u'yes':
            full_filename = 'subject-' + str(self.experiment.var.subject_nr) + '_marker_table'
            self.get_marker_manager().save_marker_table(filename=full_filename,
                                                        location=self.experiment.experiment_path,
                                                        more_info={'Device tag': self.get_tag(),
                                                                   'Subject': self.experiment.var.subject_nr})

        # Close marker device:
        self.close()

        # Get marker tables and save in var
        marker_df, summary_df, error_df = self.get_marker_manager().gen_marker_table()
        self.experiment.var.marker_df = marker_df
        self.experiment.var.summary_df = summary_df
        self.experiment.var.error_df = error_df

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

        if self.get_device() == 'ANY':
            device_type = ''
        else:
            device_type = self.get_device()

        if self.get_addr() == 'ANY':
            addr = ''
        else:
            addr = self.get_addr()

        if self.get_serial() == 'ANY':
            serialno = ''
        else:
            serialno = self.get_serial()

        # Find device
        try:
            device_info = mark.find_device(device_type=device_type,
                                           serial_no=serialno,
                                           com_port=addr,
                                           fallback_to_fake=False)
        except:
            raise osexception(f"Marker device init error: {sys.exc_info()[1]}")

        return device_info


class qtmarkers_init(markers_init, qtautoplugin):
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
        markers_init.__init__(self, name, experiment, script)
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

        device_tag = self.get_tag()

        if not(bool(re.match("^[A-Za-z0-9_-]*$", device_tag)) and bool(re.match("^[A-Za-z]*$", device_tag[0]))):
            self.extension_manager.fire('notify',
                                        message='<strong>Warning</strong>: '
                                                "Device tag can only contain letters, numbers, underscores and dashes "
                                                "and should start with a letter.",
                                        category='warning',
                                        timeout=10000,
                                        always_show=True)
