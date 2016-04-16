import os, sys
import config,twitter
import wx
class EventsGui(wx.Frame):

	def __init__(self):

		wx.Frame.__init__(self, None, title="Events", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.events_box = wx.BoxSizer(wx.VERTICAL)
		self.eventslist_label=wx.StaticText(self.panel, -1, "Events")
		self.eventslist = wx.ListBox(self.panel, -1)
		self.events_box.Add(self.eventslist, 0, wx.ALL, 10)
		for i in range(0,len(twitter.events)):
			self.eventslist.Insert(twitter.events[i],self.eventslist.GetCount())
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def OnClose(self, event):
		self.Destroy()