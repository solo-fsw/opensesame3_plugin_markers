# Metadata for package. Used in setup.py and plugin files.

version = "0.1.2"
name = "opensesame-plugin-markers"
description = "Plugin for controlling Leiden Univ marker devices."
url = "https://github.com/solo-fsw/opensesame_plugin_markers"
author = "SOLO Research Support FSW Leiden"
author_email = "labsupport@FSW.leidenuniv.nl"
install_requires="marker-management @ git+https://github.com/solo-fsw/python-markers.git@ca5f18940f67c8f0ee741b5a94b6936c36d7812d"