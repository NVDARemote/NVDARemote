# NVDA Add-on Scons Template #

This package contains a basic template structure for NVDA add-on development, building, distribution and localization.
For details about NVDA add-on development please see the [NVDA Developer Guide](http://www.nvda-project.org/documentation/developerGuide.html).
The NVDA addon development/discussion list [is here](https://nvda-addons.groups.io/g/nvda-addons)

Copyright (C) 2012-2019 nvda addon team contributors.

This package is distributed under the terms of the GNU General Public License, version 2 or later. Please see the file COPYING.txt for further details.

## Features

This template provides the following features you can use to help NVDA add-on development:

* Automatic add-on package creation, with naming and version loaded from a centralized build variables file (buildVars.py).
* Manifest file creation using a template (manifest.ini.tpl). Build variables are replaced on this template.
* Compilation of gettext mo files before distribution, when needed.
	* To generate a gettext pot file, please run scons pot. A **addon-name.pot** file will be created with all gettext messages for your add-on. You need to check the buildVars.i18nSources variable to comply with your requirements.
* Automatic generation of manifest localization files directly from gettext po files. Please make sure buildVars.py is included in i18nFiles.
* Automatic generation of HTML documents from markdown (.md) files, to manage documentation in different languages.

## Requirements

You need the following software to use this code for your NVDA add-ons development:

* a Python distribution (2.7 or greater is recommended). Check the [Python Website](http://www.python.org) for Windows Installers.
* Scons - [Website](http://www.scons.org/) - version 2.1.0 or greater. Install it using **easy_install** or grab an windows installer from the website.
* GNU Gettext tools, if you want to have localization support for your add-on - Recommended. Any Linux distro or cygwin have those installed. You can find windows builds [here](http://gnuwin32.sourceforge.net/downlinks/gettext.php).
* Markdown-2.0.1 or greater, if you want to convert documentation files to HTML documents. You can [Download Markdown-2.0.1 installer for Windows](https://pypi.python.org/pypi/Markdown/2.0.1) or get it using `easy_install markdown`.

## Usage

### To create a new NVDA add-on, taking advantage of this template:

1. Create an empty folder to hold the files for your add-on.
2. Copy the **site_scons** folder, and the following files, into your new empty folder: **buildVars.py**, **manifest.ini.tpl**, **manifest-translated.ini.tpl**, **sconstruct**, **.gitignore**, and **.gitattributes**
3. Create an **addon** folder inside your new folder. Inside the **addon* folder, create needed folders for the add-on modules (e.g. appModules, synthDrivers, etc.). An add-on may have one or more module folders.
4. In the **buildVars.py** file, change variable **addon_info** with your add-on's information (name, summary, description, version, author and url).
5. Put your code in the usual folders for NVDA extension, under the **addon** folder. For instance: globalPlugins, synthDrivers, etc.
6. Gettext translations must be placed into addon\locale\<lang>/LC_MESSAGES\nvda.po. 

### To manage documentation files for your addon:

1. Copy the **readme.md** file for your add-on to the first created folder, where you copied **buildVars.py**. You can also copy **style.css** to improve the presentation of HTML documents.
2. Documentation files (named **readme.md**) must be placed into addon\doc\<lang>/.

+### To package the add-on for distribution:

1. Open a command line, change to the folder that has the **sconstruct** file (usually the root of your add-on development folder) and run the **scons** command. The created add-on, if there were no errors, is placed in the current directory.
2. You can further customize variables in the **buildVars.py** file.

Note that this template only provides a basic add-on structure and build infrastructure. You may need to adapt it for your specific needs.

If you have any issues please use the NVDA addon list mentioned above.
