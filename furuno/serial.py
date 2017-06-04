import os
import wx
import wx.xrc
from pubsub import pub
from serial.threaded import LineReader, ReaderThread


class PrintLines(LineReader):

    def connection_made(self, transport):
        super(PrintLines, self).connection_made(transport)
        wx.CallAfter(pub.sendMessage, "update", msg='##info Connected to COM port ')

    def handle_line(self, data):
        wx.CallAfter(pub.sendMessage, "update", msg=data)

    def connection_lost(self, exc):
        if exc:
            wx.CallAfter(pub.sendMessage, "update", msg='##error: Lost connection to COM port')

    def searchcom(self):

        # chose an implementation, depending on os
        # ~ if sys.platform == 'cli':
        # ~ else:
        if os.name == 'nt':  # sys.platform == 'win32':
            from serial.tools.list_ports_windows import comports
        elif os.name == 'posix':
            from serial.tools.list_ports_posix import comports
        # ~ elif os.name == 'java':
        else:
            raise ImportError(
                "Sorry: no implementation for COM ports for your platform ('{}') available".format(os.name))
        iterator = sorted(comports())
        return ["{:20}".format(data[0]).strip() for data in iterator]
