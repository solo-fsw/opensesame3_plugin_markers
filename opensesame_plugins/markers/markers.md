# ParMarker Plug-in for OpenSesame
Hello. 🤖

# Initializing the ParMarker
Add a ParMarker object to the start of your experiment. Set this object's mode to "Initialize ParMarker". This will initialize a ParMarker device. This object must run before subsequent ParMarker objects can send markers.

A ParMarker object in "Initialize ParMarker" mode will connect to a ParMarker device. Subsequent ParMarker objects in "Send marker" mode will use this ParMarker device to send markers.

Generally, only a single ParMarker object can have its mode set to "Initialize ParMarker". If you wish to use multiple ParMarker devices, see below.
## Initialization Settings


# Sending Markers:
To send a marker, add a ParMarker object to the place in your experiment where you would like to send a marker. This object's mode must be set to "Send marker".

## Settings for Sending Markers

# Object Placement and Timing