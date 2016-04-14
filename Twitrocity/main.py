import wx
app = wx.App(redirect=False)
from gui import interface
import twitter
import config
import speak


config.setup()
speak.speak("Logging in...")
twitter.Setup()
interface.window.Show()
speak.speak("loading timelines...")
twitter.backfill()
twitter.check_streams()
app.MainLoop()