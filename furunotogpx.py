# -*- coding: utf-8 -*-

import os
import wx
import wx.xrc
from furuno.events import EventFrame

app = wx.App(False)

# create an object
frame = EventFrame (None)
# show the frame
frame.Show(True)
# start the applications
app.MainLoop()