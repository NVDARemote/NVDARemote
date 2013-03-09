# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# add-on Name
	"addon-name" : "addon-template",
	# Add-on description
	# TRANSLATORS: Summary for this add-on to be shown on installation and add-on information.
	"addon-summary" : _("Add-on quick summary"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on installation and add-on information
	"addon-description" : _("""Description for the add-on.
It can span multiple lines."""),
	# version
	"addon-version" : "x.y.z",
	# Author(s)
	"addon-author" : "name <name@domain.com>",
	# URL for the add-on documentation support
	"addon-url" : None
}


import os.path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = []

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []
