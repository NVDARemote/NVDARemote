# -*- coding: UTF-8 -*-

# docHandler: module for managing addons documentation
# See: http://community.nvda-project.org/ticket/2694

import os
import languageHandler
import addonHandler
import globalPluginHandler
import gui
import wx

addonHandler.initTranslation()

_addonDir = os.path.join(os.path.dirname(__file__), "..").decode("mbcs") # The root of an addon folder
_docFileName = "readme.html" # The name of an addon documentation file
_curAddon = addonHandler.Addon(_addonDir) # Addon instance
_addonSummary = _curAddon.manifest['summary']
_addonVersion = _curAddon.manifest['version']
_addonName = _curAddon.manifest['name']

def getDocFolder(addonDir=_addonDir):
	langs = [languageHandler.getLanguage(), "en"]
	for lang in langs:
		docFolder = os.path.join(addonDir, "doc", lang)
		if os.path.isdir(docFolder):
			return docFolder
		if "_" in lang:
			tryLang = lang.split("_")[0]
			docFolder = os.path.join(addonDir, "doc", tryLang)
			if os.path.isdir(docFolder):
				return docFolder
			if tryLang == "en":
				break
		if lang == "en":
			break
	return None

def getDocPath(docFileName=_docFileName):
	docPath = getDocFolder()
	if docPath is not None:
		docFile = os.path.join(docPath, docFileName)
		if os.path.isfile(docFile):
			docPath = docFile
	return docPath

def openDocPath():
	try:
		os.startfile(getDocPath())
	except WindowsError:
		pass

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		self.help = gui.mainFrame.sysTrayIcon.helpMenu
		self.helpItem = self.help.Append(wx.ID_ANY, u"{summary} {version}".format(summary=_addonSummary, version=_addonVersion), _addonName)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onHelp, self.helpItem)

	def onHelp(self, evt):
		openDocPath()

	def terminate(self):
		try:
			self.help.RemoveItem(self.helpItem)
		except wx.PyDeadObjectError:
			pass
