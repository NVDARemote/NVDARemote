import wx

import gui


class RemoteMenu(wx.Menu):
    """Menu for the NVDA Remote addon that appears in the NVDA Tools menu"""

    connectItem: wx.MenuItem
    disconnectItem: wx.MenuItem
    muteItem: wx.MenuItem
    pushClipboardItem: wx.MenuItem
    copyLinkItem: wx.MenuItem
    sendCtrlAltDelItem: wx.MenuItem
    remoteItem: wx.MenuItem

    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
        # Translators: Item in NVDA Remote submenu to connect to a remote computer.
        self.connectItem: wx.MenuItem = self.Append(
            wx.ID_ANY,
            _("Connect..."),
            _("Remotely connect to another computer running NVDA Remote Access"),
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.client.doConnect, self.connectItem
        )
        # Translators: Item in NVDA Remote submenu to disconnect from a remote computer.
        self.disconnectItem: wx.MenuItem = self.Append(
            wx.ID_ANY,
            _("Disconnect"),
            _("Disconnect from another computer running NVDA Remote Access"),
        )
        self.disconnectItem.Enable(False)
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.onDisconnectItem, self.disconnectItem
        )
        # Translators: Menu item in NvDA Remote submenu to mute speech and sounds from the remote computer.
        self.muteItem: wx.MenuItem = self.Append(
            wx.ID_ANY,
            _("Mute remote"),
            _("Mute speech and sounds from the remote computer"),
            kind=wx.ITEM_CHECK,
        )
        self.muteItem.Enable(False)
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onMuteItem, self.muteItem)
        # Translators: Menu item in NVDA Remote submenu to push clipboard content to the remote computer.
        self.pushClipboardItem: wx.MenuItem = self.Append(
            wx.ID_ANY,
            _("&Push clipboard"),
            _("Push the clipboard to the other machine"),
        )
        self.pushClipboardItem.Enable(False)
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.onPushClipboardItem, self.pushClipboardItem
        )
        # Translators: Menu item in NVDA Remote submenu to copy a link to the current session.
        self.copyLinkItem: wx.MenuItem = self.Append(
            wx.ID_ANY, _("Copy &link"), _("Copy a link to the remote session")
        )
        self.copyLinkItem.Enable(False)
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.onCopyLinkItem, self.copyLinkItem
        )
        # Translators: Menu item in NVDA Remote submenu to send Control+Alt+Delete to the remote computer.
        self.sendCtrlAltDelItem: wx.MenuItem = self.Append(
            wx.ID_ANY, _("Send Ctrl+Alt+Del"), _("Send Ctrl+Alt+Del")
        )
        gui.mainFrame.sysTrayIcon.Bind(
            wx.EVT_MENU, self.onSendCtrlAltDel, self.sendCtrlAltDelItem
        )
        self.sendCtrlAltDelItem.Enable(False)
        # Translators: Label of menu in NVDA tools menu.
        self.remoteItem = toolsMenu.AppendSubMenu(
            self, _("R&emote"), _("NVDA Remote Access")
        )

    def terminate(self) -> None:
        self.Remove(self.connectItem.Id)
        self.connectItem.Destroy()
        self.connectItem = None
        self.Remove(self.disconnectItem.Id)
        self.disconnectItem.Destroy()
        self.disconnectItem = None
        self.Remove(self.muteItem.Id)
        self.muteItem.Destroy()
        self.muteItem = None
        self.Remove(self.pushClipboardItem.Id)
        self.pushClipboardItem.Destroy()
        self.pushClipboardItem = None
        self.Remove(self.copyLinkItem.Id)
        self.copyLinkItem.Destroy()
        self.copyLinkItem = None
        self.Remove(self.sendCtrlAltDelItem.Id)
        self.sendCtrlAltDelItem.Destroy()
        self.sendCtrlAltDelItem = None
        tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
        tools_menu.Remove(self.remoteItem.Id)
        self.remoteItem.Destroy()
        self.remoteItem = None
        try:
            self.Destroy()
        except (RuntimeError, AttributeError):
            pass

    def onDisconnectItem(self, evt: wx.CommandEvent) -> None:
        evt.Skip()
        self.client.disconnect()

    def onMuteItem(self, evt: wx.CommandEvent) -> None:
        evt.Skip()
        self.client.toggleMute()

    def onPushClipboardItem(self, evt: wx.CommandEvent) -> None:
        evt.Skip()
        self.client.pushClipboard()

    def onCopyLinkItem(self, evt: wx.CommandEvent) -> None:
        evt.Skip()
        self.client.copyLink()

    def onSendCtrlAltDel(self, evt: wx.CommandEvent) -> None:
        evt.Skip()
        self.client.sendSAS()

    def handleConnected(self, connected: bool) -> None:
        self.connectItem.Enable(not connected)
        self.disconnectItem.Enable(connected)
        self.muteItem.Enable(connected)
        if not connected:
            self.muteItem.Check(False)
        self.pushClipboardItem.Enable(connected)
        self.copyLinkItem.Enable(connected)
        self.sendCtrlAltDelItem.Enable(connected)
