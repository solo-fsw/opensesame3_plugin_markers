"""OpenSesame 4 plugin for initializing Leiden univ marker devices"""

# The category determines the group for the plugin in the item toolbar
category = "Flow control"
# Defines the GUI controls
controls = [

    {
        "type": "line_edit",
        "var": "marker_device_tag",
        "label": "Device tag",
        "name": "marker_device_tag_widget",
        "info": "Enter a tag (name) to give the marker device (do not include spaces)."
    }, {
        "type": "combobox",
        "var": "marker_device",
        "label": "Marker device",
        "options": [
            "ANY",
            "UsbParMarker",
            "Eva"
        ],
        "name": "marker_device_widget",
        "info": "The marker device type. 'ANY' will search for any device available."
    }, {
        "type": "line_edit",
        "var": "marker_device_addr",
        "label": "Device address",
        "name": "marker_device_addr_widget",
        "info": "The address of the marker device should be a COM address, e.g. COM1. If unknown, leave at default 'ANY' and the address will be found automatically."
    }, {
        "type": "line_edit",
        "var": "marker_device_serial",
        "label": "Device serial number",
        "name": "marker_device_serial_widget",
        "info": "Enter the serial number of the marker device. If unknown, leave at default 'ANY'."
    }, {
        "type": "checkbox",
        "var": "marker_crash_on_mark_errors",
        "label": "Crash on marker errors",
        "name": "marker_crash_on_mark_errors_widget",
        "info": "When checked, the task will crash when one of the following marker errors occurs: marker too short, same marker value twice, marker could not be sent to marker device."
    }, {
        "type": "checkbox",
        "var": "marker_dummy_mode",
        "label": "Dummy mode",
        "name": "marker_dummy_mode_widget",
        "info": "When checked, dummy mode will be used (no marker device needs to be connected, use for development)."
    }, {
        "type": "checkbox",
        "var": "marker_gen_mark_file",
        "label": "Generate marker file",
        "name": "marker_gen_mark_file_widget",
        "info": "When checked, a tsv file will be created containing a marker table, marker summary and errors."
    }, {
        "type": "checkbox",
        "var": "marker_flash_255",
        "label": "Flash 255",
        "name": "marker_flash_255_widget",
        "info": "When checked, two pulses with a value of 255 will be sent on initialization. Do not use with Actiview as pulses with value 255 may pause the recording."
    }

]
