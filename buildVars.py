# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "remote",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Remote Support"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""Allows remote control of and remote access to another machine."""),
	# version
	"addon_version" : "2.1",
	# Author(s)
	"addon_author" : u"Tyler Spivey <tspivey@pcdesk.net>, Christopher Toth <q@q-continuum.net>",
	# URL for the add-on documentation support
	"addon_url" : "http://NVDARemote.com",
	# Documentation file name
	"addon_docFileName" : "readme.html",
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [
	'addon/globalPlugins/*/*.py',
	'addon/globalPlugins/*/*.exe',
	'addon/globalPlugins/*/*.dll',
	'addon/synthDrivers/*/*.py',
]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = ['globalPlugins\\remoteClient\\url_handler.obj']
