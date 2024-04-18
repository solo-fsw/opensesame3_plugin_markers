# Markers plugin for OpenSesame
The markers_os3 plugin is used to send markers to different Leiden Univ FSW marker devices. See [here](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/) for more information on markers in general. Note that this plugin is only compatible with OpenSesame 3.

# Initializing the Marker Device
Add a markers_os3_init item to the start of your experiment. This item handles the initialization of the marker device and must be run before subsequent markers_os3_send items can send markers.

A markers_os3_init item will connect to a marker device. Subsequent markers_os3_send items will use this marker device to send markers. 

Generally, only a single markers_os3_init item is required. If you wish to use multiple marker devices, see below.

## Initialization Settings
- **Device tag:** The tag (name) of the device. The device tag can only contain letters, numbers, underscores and dashes and should start with a letter. To send markers to the marker device, the same tag must be used in subsequent markers_os3_send items. Use different tag names when multiple marker devices are used to differentiate between the devices.

- **Marker device:** The marker device type that should be used: [UsbParMarker](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/UsbParMarker/), [Eva](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/EVA/) or ANY (ANY searchers for any device available).

- **Device address:** The address of the port the marker device is connected to. This should be a COM address (e.g. COM1). If unknown, leave at ANY or leave empty and the address will be found automatically.

- **Device serial number:** The serial number of the marker device. If unknown, leave at ANY or leave empty and the address will be found automatically.

- **Crash on marker errors:** When checked, the task will crash on marker errors. If unchecked, the task will not crash, but the errors will be stored in a table, which can be viewed in the *Marker tables* tab at the end of the experiment, or in the marker_table TSV file that is saved when checking the *Generate marker* file setting. Marker errors consist of the following: 
    - The marker duration is too short (< 10 ms)
    - The same marker value is sent twice in a row
    - The marker was not successfully sent to the marker device

- **Dummy mode:** When checked, dummy mode is used and no actual device needs to be connected to the computer. Use for development.

- **Generate marker file:** When checked, a TSV file will be saved that contains a marker summary table, a marker table and an error table (the same tables can be viewed at the end of the experiment in the Marker tables tab). This TSV file will be saved in the same location as the log file.

- **Flash 255:** When checked, two pulses with value 255 (all bits high), each with a duration of 100 ms will be sent when initializing the marker device. Note: use with caution in combination with the BioSemi EEG system! The value 255 can unintentionally pause the recording.


# Sending Markers:
To send a marker, add a markers_os3_send item to the place in your experiment where you would like to send a marker.

## Settings for Sending Markers
- **Device tag:** The tag of the marker device that should receive the marker. This should be the same as the tag given to the device during initialization.

- **Marker value:** The marker value. Should be an integer between 0 - 255. Use attribute reference when the marker values are stored in a loop (e.g. [marker_value])

- **Object duration (ms):** The duration of the markers_os3_send item. This is not necessarily the same as the duration of the marker! Only when *Reset marker value to zero* is checked, the object duration is the same as the marker duration.

- **Reset marker value to zero:** When checked, the marker value will automatically reset to 0 after the object duration.

# Object Placement and Timing
For proper understanding of object placement and timing, it is important to note that the Markers items (markers_os3_init and markers_os3_send) do not have a visual component on the screen. Thus, during the duration of these items, what was already presented on the screen, will stay on the screen.

To obtain the most accurate timing of the marker (i.e. the marker is sent as closely near the actual event of interest as possible), use the following item placement:

For example, a marker should be sent during a stimulus, it should start exactly when the stimulus starts, and should end (i.e. reset to 0) directly after the stimulus ends. 

- Make sure a markers_os3_init item is placed at the start of the experiment.
- Place the stimulus item at the start of the trial with a duration of 0.
- Place a markers_os3_send item right after the stimulus. Set the *Marker value* to the desired value. 
- When the stimulus does not require a response, the *Object duration* of the markers_os3_send item can be set to the desired stimulus duration and the *Reset marker value to zero* can be checked. Because the markers_os3_send item does not have a visual component, the stimulus is presented during the *Object duration* of the markers_os3_send item.
- When the stimulus does require a response, it is advised to set the *Object duration* of the markers_os3_send item to 10 and leave the *Reset marker value to zero* unchecked. Place a response item (keyboard response or mouse response) after the markers_os3_send item. Since the marker has not been reset to 0 yet, another markers_os3_send item should be placed after the response item, in which value 0 is sent. This will do the following: the stimulus is presented on the screen and then the marker is sent, then the task waits until a response is collected from the participant and finally resets the marker to 0. The *Object duration* of the markers_os3_send item is set to 10 instead of 0 to have a minimum duration of 10 ms of the marker, because theoretically a participant can respond within 10 ms.

## Using Multiple Marker Devices
When multiple marker devices are used, make sure to have one markers_os3_init item per marker device and place them at the start of the experiment (it is important that all markers_os3_init items exist in the same sequence). Specify the *Device address* and/or *Device serial number* (this is usually not necessary when only one marker device is used). Give the marker devices their own tag (name), and use these tags in the markers_os3_send items to differentiate between the devices.
