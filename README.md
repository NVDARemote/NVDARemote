# NVDA Add-on Scons Template

This package contains a basic template structure for NVDA add-on development, building and distribution.
For details about NVDA add-on development please see the [NVDA Developer Guide](http://www.nvda-project.org/documentation/developerGuide.html).

Coryright (C) 2012 - Rui Batista.

This package is distributed under the terms of the GNU General Public License, version 2 or later. Please see the file COPYING.txt for further details.

## Features

This template provides the following features you can use to help NVDA add-on development:
* Automatic add-on package creation, with naming and version loaded from a centralized build variables file (buildVars.py).
* Manifest file creation using a template (manifest.ini.tpl). Build variables are replaced on this template.
* Compilation of gettext mo files before distribution, when needed.file for the needs of your add-on.
- To generate a gettext pot file, please run scons pot. a <adon-name>.pot file will be created with all gettext messages for your add-on. You need to check the buildVars.i18nSources variable to comply with your requirements.


## Requirements

You need the following software to use this code on your NVDA add-ons development:

- a Python distribution (2.7 or greater is recomended). Check the [Python Website](http://www.python.org) for Windows Installers.
- Scons - [Website](http://www.scons.org/) - version 2.1.0 or greater. Install it using **easy_install** or grab an windows installer from the website.
- GNU Gettext tools, if you want to have localization support on your add-on - Recomended. Any Linux distro or cygwin have those installed. You can find windows builds [here](http://gnuwin32.sourceforge.net/downlinks/gettext.php).

## Usage

To create a new NVDA add-on, taking advantage of this template: 

- Create an empty folder to put your add-on's files
- Copy the **addon** folder, the **buildVars.py** file, and the **SCONSTRUCT** file to the created folder
- On the **buildVars.py** file, change variable **addon_info** with your add-on's information (name, version, author and url).
- Change the **manifest.ini.tpl** file so it further reflects your add-on information that can be translated 8summary and description). Don't leave any field as is. Values between braces are variables replaced from the **addon_info** variable you have set.
- Put your code in the usual folders for NVDA extension, under the **addon** folder. For instance: globalPlugins, synthDrivers, etc. You can delete folders you don't need on your particular add-on package.
- Gettext translations must be placed into addon\locale\<lang>/LC_MESSAGES\nvda.po. Manifest translations must be ptu on **addon\locale\<lang>\manifest.ini**.
- To package the add-on for distribution, open a command line, change to the folder that as the **SCONSTRUCT** file and run the **scons** command. The created add-on, if no errors happen, is placed on the current directory.
- You can further customize variables in the **buildVars.py** file.
Note that this template only provides a basic add-on structure and build infrastructure. You may need to adapt it for your specific needs.


## Author Information

If you have any issues or whatever, please use github, bibtbucket, the NVDA development list, or just drop me an email to ruiandrebatista at gmail dot com.
