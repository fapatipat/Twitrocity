import speak
import twitter
import wx
class TweetGui(wx.Frame):

	global inittext
	global id
	global edit

	def __init__(self,inittext="",i="",ed=0):
		self.edit=ed
		self.id=i
		wx.Frame.__init__(self, None, title="Tweet", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Tweet Te&xt")
		self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.Bind(wx.EVT_TEXT_ENTER, self.Tweet)
		self.text.AppendText(inittext)
		#self.text.SetSelection(self.text.GetLastPosition()-1,self.text.GetLastPosition())
		self.text.SetMaxLength(140)
		#self.text.SetInsertionPoint(self.text.GetLastPosition())
		self.tweet = wx.Button(self.panel, wx.ID_DEFAULT, "&Send")
		self.tweet.SetDefault()
		self.tweet.Bind(wx.EVT_BUTTON, self.Tweet)
		self.main_box.Add(self.tweet, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def Tweet(self, event):
		if self.edit==1:
			twitter.Delete(self.id)
		twitter.Tweet(self.text.GetValue(),self.id)
		self.Destroy()
	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()


class QuoteGui(wx.Frame):

	global inittext
	global id

	def __init__(self,i=""):
		self.id=i
		a=twitter.api.get_status(self.id)
		self.inittext=a.text
		wx.Frame.__init__(self, None, title="Tweet", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Tweet Te&xt")
		self.text = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text2_label = wx.StaticText(self.panel, -1, "Quoting")
		self.text2 = wx.TextCtrl(self.panel, -1, "",style=wx.TE_READONLY)
		self.main_box.Add(self.text2, 0, wx.ALL, 10)
		self.text2.SetValue(self.inittext)
		self.tweet = wx.Button(self.panel, wx.ID_DEFAULT, "&Send")
		self.tweet.Bind(wx.EVT_BUTTON, self.Tweet)
		self.main_box.Add(self.tweet, 0, wx.ALL, 10)
		self.tweet.SetDefault()
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def EVT_TEXT_ENTER(self,event):
		speak.speak("Boing")
	def Tweet(self, event):
		twitter.Quote(status=self.id,text=self.text.GetValue())
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
		self.recip_label = wx.StaticText(self.panel, -1, "&Recipient")
		self.recip = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.recip, 0, wx.ALL, 10)
		self.recip.SetValue(self.user)
		self.tweet = wx.Button(self.panel, wx.ID_DEFAULT, "&Send")
		self.tweet.Bind(wx.EVT_BUTTON, self.Tweet)
		self.main_box.Add(self.tweet, 0, wx.ALL, 10)
		self.tweet.SetDefault()
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def Tweet(self, event):
		twitter.Tweet("d @"+self.recip.GetValue()+" "+self.text.GetValue(),0)
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