# Markers Plug-in for OpenSesame
With this plug-in markers can be send to different Leiden Univ FSW marker devices.

# Initializing the Marker Device
Add a Marker object to the start of your experiment. Set the object's mode to "Initialize". This will initialize the device. This object must run before subsequent Marker objects can send markers.

A Marker object in "Initialize" mode will connect to a marker device. Subsequent MArker objects in "Send marker" mode will use this Marker device to send markers.

Generally, only a single Marker object can have its mode set to "Initialize". If you wish to use multiple Marker devices, see below.

## Initialization Settings
- **Marker device:** The marker device type that should be used (ANY searchers for any device available). 


- **Device address:** The address of the port the marker device is connected to. This should be a COM address (e.g. COM1). If unknown, leave at ANY and the address will be found automatically.

- **Device serial number:** The serial number of the marker device. If unknown, leave at ANY and the address will be found automatically. 

- **Device tag:** The tag (name) of the device (must not include spaces). This tag is given to the marker device in OpenSesame. This is especially useful when multiple marker devices are used, with differnt tags these devices can be differentiated.

- **Crash on marker errors:** When checked, the task will crash on marker errors. If unchecked, the task will not crash, but the errors will be stored in a table, which can be viewed in the Marker tables tab at the end of the experiment, or in the Marker_table .tsv file that is saved when checking the Generate marker file setting. Marker errors consist of the following: The marker duration is too short (< 10 ms), the same marker value is sent twice in a row, the marker could not be sent to the marker device.

- **Dummy mode:** When checked, dummy mode is used and no actual device needs to be connected to the computer. Useful for development.

- **Generate marker file:** If checked, a .tsv file with the name subject-<subject_nr>_marker_table.tsv will be saved in the location of the OpenSesame task containing a marker summary table, marker table and error table (the same tables that can be viewed at the end of the experiment in the Marker Tables tab.)

- **Flash 255:** When checked, two pulses of value 255 (all bits high), each with a duration of 100 ms will be sent when initializing the marker device. 


# Sending Markers:
To send a marker, add a Marker object to the place in your experiment where you would like to send a marker. This object's mode must be set to "Send marker".

## Settings for Sending Markers
- **Marker device:** The marker device type that should be used (ANY searchers for any device available). 

- **Device tag:** The tag of the device that should receive the marker. This should be the same as the tag given to the device during intialization.

- **Marker value:** The marker value. Should be an integer between 0 - 255.

- **Object duration (ms):** The duration of the send_marker object. This is not the same as the duration of the marker! Only when Reset marker value to zero is checked, the object duration is the same as the marker duration. 

- **Reset marker value to zero:** When checked, the marker value will automatically reset to 0 after the object duration. Note that the duration must be minimally 5 ms. 

# Object Placement and Timing
To obtain the most accurate timing of the marker (i.e. the marker is sent as closely near the actual event of interest as possible), use the following object placement:

For example, a marker should be sent during a stimulus object, it should be high exactly when the stimulus starts, and reset to 0 after the stimulus. 

- Place the stimulus object at the start of the trial with a duration of 0.
- Place a Marker object in Send marker mode right after the stimulus. Set the Marker value to the desired value. 
- When the stimulus does not need a response, the Object duration should be set to the stimulus duration and the Reset marker value to zero should be checked. 
- Or, when the stimulus does require a response, the Object duration should be set to 0 and the Reset to marker value should be unchecked. After this object, place a response object (keyboard response, or mouse response). Since the marker has not been reset to 0 yet, another Send marker object should be placed after the response object, in which value 0 is sent. 
