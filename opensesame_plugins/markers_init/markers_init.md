# Markers Plug-in for OpenSesame
The Markers plug-in is used to send markers to different Leiden Univ FSW marker devices.

# Initializing the Marker Device
Add a markers_init object to the start of your experiment. This object handles the initialization of the marker device. This object must run before subsequent markers_send objects can send markers.

A markers_init object  will connect to a marker device. Subsequent markers_send objects will use this marker device to send markers.

Generally, only a single markers_init object is required. If you wish to use multiple marker devices, see below.

## Initialization Settings
- **Device tag:** The tag (name) of the device (cannot include spaces). To send markers to the marker device, the same tag must be used in subsequent markers_send objects. Use different tag names when multiple marker devices are used to differentiate between the devices.

- **Marker device:** The marker device type that should be used (ANY searchers for any device available). 

- **Device address:** The address of the port the marker device is connected to. This should be a COM address (e.g. COM1). If unknown, leave at ANY and the address will be found automatically.

- **Device serial number:** The serial number of the marker device. If unknown, leave at ANY and the address will be found automatically. 

- **Crash on marker errors:** When checked, the task will crash on marker errors. If unchecked, the task will not crash, but the errors will be stored in a table, which can be viewed in the *Marker tables* tab at the end of the experiment, or in the marker_table TSV file that is saved when checking the *Generate marker* file setting. Marker errors consist of the following: 
    - The marker duration is too short (< 10 ms)
    - The same marker value is sent twice in a row
    - The marker was not successfully sent to the marker device

- **Dummy mode:** When checked, dummy mode is used and no actual device needs to be connected to the computer. Use for development.

- **Generate marker file:** When checked, a TSV file will be saved that contains a marker summary table, a marker table and an error table (the same tables can be viewed at the end of the experiment in the Marker tables tab). This TSV file will be saved in the same location as the OpenSesame task.

- **Flash 255:** When checked, two pulses with value 255 (all bits high), each with a duration of 100 ms will be sent when initializing the marker device. 


# Sending Markers:
To send a marker, add a markers_send object to the place in your experiment where you would like to send a marker.

## Settings for Sending Markers
- **Device tag:** The tag of the marker device that should receive the marker. This should be the same as the tag given to the device during intialization.

- **Marker value:** The marker value. Should be an integer between 0 - 255. Use attribute reference when the marker values are stored in a loop (e.g. [marker_value])

- **Object duration (ms):** The duration of the markers_send object. This is not necessarily the same as the duration of the marker! Only when *Reset marker value to zero* is checked, the object duration is the same as the marker duration. 

- **Reset marker value to zero:** When checked, the marker value will automatically reset to 0 after the object duration. Note that the duration must be minimally 5 ms. 

# Object Placement and Timing
To obtain the most accurate timing of the marker (i.e. the marker is sent as closely near the actual event of interest as possible), use the following object placement:

For example, a marker should be sent during a stimulus object, it should start exactly when the stimulus starts, and should end (i.e. reset to 0) directly after the stimulus ends. 

- Make sure a markers_init object is placed at the start of the experiment.
- Place the stimulus object at the start of the trial with a duration of 0.
- Place a markers_send object right after the stimulus. Set the *Marker value* to the desired value. 
- When the stimulus does not require a response, the *Object duration* can be set to the stimulus duration and the *Reset marker value to zero* can be checked. 
- When the stimulus does require a response, the *Object duration* should be set to 0 and the *Reset marker value to zero* should be unchecked. Place a response object (keyboard response or mouse response) after the markers_send object. Since the marker has not been reset to 0 yet, another markers_send object should be placed after the response object, in which value 0 is sent. 

## Using Multiple Marker Devices
When multiple marker devices are used, make sure to have one markers_init object per marker device. Specify the *Device address* or *Device serial number* (this is usually not necessary when only one marker device is used). Give the marker devices their own tag (name), and use these tags in the markers_send objects to diffentiate between the devices.