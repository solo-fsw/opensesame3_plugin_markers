# Metadata for package. Used in setup.py and plugin files.

version = "0.1.3"
name = "opensesame3-plugin-markers"
description = "OpenSesame 3 plugin for controlling Leiden Univ marker devices."
url = "https://github.com/solo-fsw/opensesame3_plugin_markers"
author = "SOLO Research Support FSW Leiden"
author_email = "labsupport@FSW.leidenuniv.nl"
install_requires=[
    "python-opensesame>=3.3, <4",
    "marker-management @ git+https://github.com/solo-fsw/python-markers.git@7dd3cfa27125116d15c213f05673bd1c9757100a"]
