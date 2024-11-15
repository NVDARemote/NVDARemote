# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guidelines.txt
	# add-on Name, internal for nvda
	"addon_name" : "remote",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("Remote Support"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""Allows remote control of and remote access to another machine."""),
	# version
	"addon_version" : "2.6.4",
	# Author(s)
	"addon_author" : u"Tyler Spivey <tspivey@pcdesk.net>, Christopher Toth <q@q-continuum.net>",
	# URL for the add-on documentation support
	"addon_url" : "https://NVDARemote.com",
	# URL for the add-on repository where the source code can be found
	"addon_sourceURL": "https://github.com/nvdaremote/nvdaremote",
	# Documentation file name
	"addon_docFileName" : "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0", minor version is optional)
	"addon_minimumNVDAVersion": "2024.1",
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion": "2024.1",
	# Add-on update channel (default is None, denoting stable releases, and for development releases, use "dev"; do not change unless you know what you are doing)
	"addon_updateChannel" : None,
	# Add-on license such as GPL 2
	"addon_license": "GPL v2",
	# URL for the license document the ad-on is licensed under
	"addon_licenseURL": "https://www.gnu.org/licenses/gpl-2.0.html",
}
import os
if os.environ.get('CI') and os.environ.get('GITHUB_REF_TYPE') == 'tag':
	addon_info['addon_version'] = os.environ['GITHUB_REF_NAME'].lstrip('v')

import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [
	'addon/globalPlugins/*/*.py',
	'addon/globalPlugins/*/*.exe',
	'addon/synthDrivers/*/*.py',
	'addon/sounds/*.wav',
]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = ['globalPlugins\\remoteClient\\url_handler.obj']

# Base language for the NVDA add-on
# If your add-on is written in a language other than english, modify this variable.
# For example, set baseLanguage to "es" if your add-on is primarily written in spanish.
baseLanguage = "en"

# Markdown extensions for add-on documentation
# Most add-ons do not require additional Markdown extensions.
# If you need to add support for markup such as tables, fill out the below list.
# Extensions string must be of the form "markdown.extensions.extensionName"
# e.g. "markdown.extensions.tables" to add tables.
markdownExtensions = []
