# Metadata for package. Used in setup.py and plugin files.

version = "0.1.2"
name = "opensesame-plugin-markers"
description = "Plugin for controlling Leiden Univ marker devices."
url = "https://github.com/solo-fsw/opensesame_plugin_markers"
author = "SOLO Research Support FSW Leiden"
author_email = "labsupport@FSW.leidenuniv.nl"
install_requires="marker-management @ git+https://github.com/solo-fsw/python-markers.git@b89a9fb2ca53f9277c7d1f99ec05f1085bbe6ce3"