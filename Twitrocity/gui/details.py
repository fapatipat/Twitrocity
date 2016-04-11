#using a different gui for this because I plan to change them just a bit.
import twitter
import wx
class DetailsGui(wx.Frame):

	global user
	def __init__(self,text,user):

		self.user=user

		wx.Frame.__init__(self, None, title="View", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Tweet Te&xt")
		self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_DONTWRAP)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetValue(text)
		self.follow = wx.Button(self.panel, -1, "&Follow "+user)
		self.follow.Bind(wx.EVT_BUTTON, self.Follow)
		self.unfollow = wx.Button(self.panel, -1, "&Unfollow "+user)
		self.unfollow.Bind(wx.EVT_BUTTON, self.Unfollow)
		self.main_box.Add(self.follow, 0, wx.ALL, 10)
		self.main_box.Add(self.unfollow, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def Follow(self, event):
		twitter.Follow(self.user)
	def Unfollow(self, event):
		twitter.Unfollow(self.user)
	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()