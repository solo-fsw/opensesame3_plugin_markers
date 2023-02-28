# Plugin for OpenSesame for sending markers
This is an OpenSesame plugin for sending markers with Leiden University devices. 

> **Note**
> This plugin is only available for Windows. 

## Installation
These installation instructions will install the Markers plugin in the Users folder `C:\Users\\%USERNAME%\AppData\Roaming\Python\share`. When different users need to use the plugin on one computer, they must all install the plugin separately.

- Make sure Git is installed.

- In OpenSesame, run from the Console:

    `!pip install --user git+https://github.com/solo-fsw/opensesame_plugin_markers`

- Restart OpenSesame. 

- The Markers items should now be visible in the Items Toolbar:

    ![markers_init](/opensesame_plugins/markers_init/markers_init_large.png)
    ![markers_send](/opensesame_plugins/markers_send/markers_send_large.png)

## How to use
Help and instructions on how to use the plugin can be found [here](https://github.com/solo-fsw/opensesame_plugin_markers/blob/main/opensesame_plugins/markers_init/markers_init.md) and in OpenSesame it can be found after inserting a markers item in your experiment by clicking on the blue questionmark in the upper right corner of the markers item tab. ![image](https://user-images.githubusercontent.com/56065641/217841460-634aee68-7b98-4154-8275-ac75337788e7.png).

In the samples folder a sample task can be found, which can also be downloaded [here](https://downgit.github.io/#/home?url=https://github.com/solo-fsw/opensesame_plugin_markers/tree/main/samples) (download starts immediately using DownGit).

## Timing test
The timing of the plugin was checked by comparing the onset of a pulse sent with the plugin to the UsbParMarker with the onset of a pulse sent to the LPT the port. Both signals were recorded with BIOPAC in AcqKnowledge. An average difference of 150 us (max 160 us) was found when sending a pulse first to the LPT port, then to the UsbParMarker and an average difference of 90 us (max 120 us) was found when sending a pulse first to the UsbParMarker, then to the LPT port (10 trials each). See the timing_test folder for the test files.

