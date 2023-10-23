# Metadata for package. Used in setup.py and plugin files.

version = "0.1.2"
name = "opensesame-plugin-markers"
description = "Plugin for controlling Leiden Univ marker devices."
url = "https://github.com/solo-fsw/opensesame_plugin_markers"
author = "SOLO Research Support FSW Leiden"
author_email = "labsupport@FSW.leidenuniv.nl"
install_requires=[
    "python>=3.7",
    "python-opensesame>=3.3, <4",
    "marker-management @ git+https://github.com/solo-fsw/python-markers.git@7dd3cfa27125116d15c213f05673bd1c9757100a"]