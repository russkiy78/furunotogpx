# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Apr 24 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Furuno <-> GPX  Converter", pos=wx.DefaultPosition,
                          size=wx.Size(500, 230), style=wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_notebook7 = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_notebook7.SetMinSize(wx.Size(-1, 100))

        self.m_panelU = wx.Panel(self.m_notebook7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer3 = wx.GridSizer(2, 2, 10, 10)

        self.m_staticText5 = wx.StaticText(self.m_panelU, wx.ID_ANY, u"Choose .gpx file for upload to Furuno",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        gSizer3.Add(self.m_staticText5, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.m_fileUpload = wx.FilePickerCtrl(self.m_panelU, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.gpx",
                                              wx.DefaultPosition, wx.DefaultSize,
                                              wx.FLP_FILE_MUST_EXIST | wx.FLP_OPEN | wx.FLP_USE_TEXTCTRL)
        gSizer3.Add(self.m_fileUpload, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_buttonUStart = wx.Button(self.m_panelU, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonUStart.Enable(False)

        gSizer3.Add(self.m_buttonUStart, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.m_buttonUStop = wx.Button(self.m_panelU, wx.ID_ANY, u"STOP", wx.Point(-1, -1), wx.DefaultSize, 0)
        self.m_buttonUStop.Enable(False)

        gSizer3.Add(self.m_buttonUStop, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.m_panelU.SetSizer(gSizer3)
        self.m_panelU.Layout()
        gSizer3.Fit(self.m_panelU)
        self.m_notebook7.AddPage(self.m_panelU, u"Upload to Furuno", True)
        self.m_panelD = wx.Panel(self.m_notebook7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer4 = wx.GridSizer(2, 2, 10, 10)

        self.m_staticText9 = wx.StaticText(self.m_panelD, wx.ID_ANY, u"Choose .gpx file for download from Furuno",
                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        gSizer4.Add(self.m_staticText9, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_fileDownload = wx.FilePickerCtrl(self.m_panelD, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.gpx",
                                                wx.DefaultPosition, wx.DefaultSize,
                                                wx.FLP_OVERWRITE_PROMPT | wx.FLP_SAVE | wx.FLP_USE_TEXTCTRL)
        gSizer4.Add(self.m_fileDownload, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_buttonDStart = wx.Button(self.m_panelD, wx.ID_ANY, u"START", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonDStart.Enable(False)

        gSizer4.Add(self.m_buttonDStart, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.m_buttonDStop = wx.Button(self.m_panelD, wx.ID_ANY, u"STOP", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_buttonDStop.Enable(False)

        gSizer4.Add(self.m_buttonDStop, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.m_panelD.SetSizer(gSizer4)
        self.m_panelD.Layout()
        gSizer4.Fit(self.m_panelD)
        self.m_notebook7.AddPage(self.m_panelD, u"Download to PC", False)

        bSizer3.Add(self.m_notebook7, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        gSizer2 = wx.GridSizer(1, 4, 0, 0)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"COM port", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        gSizer2.Add(self.m_staticText3, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        m_comportChoices = []
        self.m_comport = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_comportChoices, 0)
        self.m_comport.SetSelection(0)
        self.m_comport.SetMinSize(wx.Size(100, -1))

        gSizer2.Add(self.m_comport, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"COM port speed", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gSizer2.Add(self.m_staticText4, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        m_comspeedChoices = [u"115200", u"57600", u"38400", u"19200", u"9600", u"4800"]
        self.m_comspeed = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_comspeedChoices, 0)
        self.m_comspeed.SetSelection(2)
        self.m_comspeed.SetMinSize(wx.Size(100, -1))

        gSizer2.Add(self.m_comspeed, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer3.Add(gSizer2, 1, wx.ALIGN_CENTER | wx.EXPAND, 5)

        gSizer41 = wx.GridSizer(1, 1, 0, 0)

        self.m_state = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_state.Enable(False)
        self.m_state.SetMinSize(wx.Size(480, -1))

        gSizer41.Add(self.m_state, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        bSizer3.Add(gSizer41, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def YesNo(parent, question, caption='Yes or no?'):
        dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
        result = dlg.ShowModal() == wx.ID_YES
        dlg.Destroy()
        return result

    def Info(parent, message, caption='Insert program title'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def Warn(parent, message, caption='Warning!'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

    def Error(parent, message, caption='Error!'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
