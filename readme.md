# Plugin for OpenSesame for sending markers
This is an OpenSesame plugin for sending markers with Leiden University devices. This plugin uses the marker_management module from the python markers repo: https://github.com/solo-fsw/python-markers

> [!IMPORTANT]
> - Before following the instructions, make sure Git is installed, see https://git-scm.com/downloads.
> - This plugin is only available for Windows. 
> - This plugin is only available for OpenSesame 3. The markers plugin for OpenSesame 4 can be found here: [https://github.com/>  solo-fsw/opensesame4_plugin_markers](https://github.com/solo-fsw/opensesame4_plugin_markers)

## Installation
How the markers package can best be installed depends on the OpenSesame installation and whether it is installed system-wide (available for all users of the pc, usually through the Start menu), or whether it is installed in a Conda environment.

### OpenSesame system installation
When using a system-wide installation of OpenSesame, the plugin can be installed in the Users folder `C:\Users\%USERNAME%\AppData\Roaming\Python\Python37\site-packages`. To do so, the `--user` flag must be used when installing the plugin with `pip install`. When different users need to use the plugin on one computer, they must all install the plugin separately.

- Open the system installation of OpenSesame (e.g. from the Start menu). 

- In OpenSesame, run from the Console:

    `!pip install --user git+https://github.com/solo-fsw/opensesame3_plugin_markers`

- Restart OpenSesame. 

- The Markers items should now be visible in the Items Toolbar:

    ![markers_init](/share/opensesame_plugins/markers_os3_init/markers_os3_init_large.png)
    ![markers_send](/share/opensesame_plugins/markers_os3_send/markers_os3_send_large.png)

### OpenSesame in Conda environment
When using OpenSesame that was installed in a Conda environment, the plugin should be installed in that environment. When you use different environments, the plugin needs to be installed in each of the environments. The plugin is not installed per user, therefore, do not use the `--user` flag when installing the plugin with `pip install`.

- Start OpenSesame in the Conda environment.

- In OpenSesame, run from the Console:

     `!pip install git+https://github.com/solo-fsw/opensesame3_plugin_markers`

- Restart OpenSesame. 

- The Markers items should now be visible in the Items Toolbar:

    ![markers_init](/share/opensesame_plugins/markers_os3_init/markers_os3_init_large.png)
    ![markers_send](/share/opensesame_plugins/markers_os3_send/markers_os3_send_large.png)

### Troubleshooting:
**Git not found:** If you receive the following error when trying to install the markers plugin: `ERROR: Cannot find command 'git' - do you have 'git' installed and in your PATH?`:
- Make sure you have Git installed, see https://git-scm.com/downloads
- When you have Git installed, it may be necessary to add Git to your path. To do so, in OpenSesame run from the Console:
    - `import os`
    - `os.environ["PATH"] += os.pathsep + r"<PATH TO GIT>"` where `<PATH TO GIT>` is the path to the Git application. Usually, when Git is installed system wide, Git is located in Program Files. In this case, type `os.environ["PATH"] += os.pathsep + r"C:\Program Files\Git\cmd"`
- Then, try installing the markers plugin again.

## How to use
Help and instructions on how to use the plugin can be found [here](/share/opensesame_plugins/markers_os3_init/markers_os3_init.md) and in OpenSesame it can be found after inserting a markers item in your experiment by clicking on the blue questionmark in the upper right corner of the markers item tab. ![image](https://user-images.githubusercontent.com/56065641/217841460-634aee68-7b98-4154-8275-ac75337788e7.png).

In the samples folder a sample task can be found, which can also be downloaded [here](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Fsolo-fsw%2Fopensesame3_plugin_markers%2Ftree%2Fmain%2Fsamples) (download starts immediately).

## Timing test
The timing of the plugin was tested by comparing the onset of a pulse sent with the plugin to the UsbParMarker with the onset of a pulse sent to the LPT port (the original way of sending markers). Both signals were recorded with BIOPAC in AcqKnowledge. An average difference of 133 us (range 100 us - 300 us) was found when sending a pulse first to the LPT port, then to the UsbParMarker and an average difference of 236 us (range 140 us - 360 us) was found when sending a pulse first to the UsbParMarker, then to the LPT port (20 trials each). See the timing_test folder for the experiment used and the AcqKnowledge data files. 

## References
- [SOLO wiki on markers](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/)
- [Python markers github page](https://github.com/solo-fsw/python-markers)
- [OpenSesame 4 Markers plugin](https://github.com/solo-fsw/opensesame4_plugin_markers)
- [SOLO wiki on the UsbParMarker](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/UsbParMarker/)
- [SOLO wiki on Eva](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/EVA/)
- [UsbParMarker github page](https://github.com/solo-fsw/UsbParMarker)
- [Eva github page](https://github.com/solo-fsw/Eva)
