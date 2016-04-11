import twitter
import wx
class ProfileGui(wx.Frame):

	def __init__(self):
		s=twitter.api.me()
		wx.Frame.__init__(self, None, title="Profile Editor", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.name_label = wx.StaticText(self.panel, -1, "Full Name")
		self.name = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.name, 0, wx.ALL, 10)
		if s.name!=None:
			self.name.SetValue(s.name)
		self.url_label = wx.StaticText(self.panel, -1, "URL")
		self.url = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.url, 0, wx.ALL, 10)
		if s.url!=None:
			self.url.SetValue(twitter.unshorten(s.url))
		self.location_label = wx.StaticText(self.panel, -1, "Location")
		self.location = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.location, 0, wx.ALL, 10)
		if s.location!=None:
			self.location.SetValue(s.location)
		self.description_label = wx.StaticText(self.panel, -1, "Description")
		self.description = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.description, 0, wx.ALL, 10)
		if s.description!=None:
			self.description.SetValue(s.description)
		self.update = wx.Button(self.panel, wx.ID_DEFAULT, "&Update")
		self.update.Bind(wx.EVT_BUTTON, self.Update)
		self.main_box.Add(self.update, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def Update(self, event):
		twitter.UpdateProfile(self.name.GetValue(),self.url.GetValue(),self.location.GetValue(),self.description.GetValue())
		self.Destroy()
	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()


class DMGui(wx.Frame):

	global user
	def __init__(self,i=""):
		self.user=i

		wx.Frame.__init__(self, None, title="Message", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Tweet Te&xt")
		self.text = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.tweet = wx.Button(self.panel, wx.ID_DEFAULT, "&Send to "+self.user)
		self.tweet.Bind(wx.EVT_BUTTON, self.Tweet)
		self.main_box.Add(self.tweet, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def Tweet(self, event):
		twitter.Tweet("d @"+self.user+" "+self.text.GetValue(),0)
		self.Destroy()
	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()

class ViewGui(wx.Frame):

	def __init__(self,text):

		wx.Frame.__init__(self, None, title="View", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Tweet Te&xt",style=wx.TE_READONLY|wx.TE_MULTILINE)
		self.text = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetValue(text)
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()