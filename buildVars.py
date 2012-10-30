# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Add-on information variables
addon_info = {
# add-on Name
	"addon-name" : "addon-template",
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
i18nSources = pythonSources 

