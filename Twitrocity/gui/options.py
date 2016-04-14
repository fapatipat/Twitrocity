import os, sys
import config,twitter
import wx
class OptionsGui(wx.Frame):

	def __init__(self):

		wx.Frame.__init__(self, None, title="Options", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.soundpack_box = wx.BoxSizer(wx.VERTICAL)
		self.soundpacklist_label=wx.StaticText(self.panel, -1, "Soundpacks")
		self.soundpackslist = wx.ListBox(self.panel, -1)
		self.soundpackslist.Bind(wx.EVT_LISTBOX, self.on_soundpacks_list_change)
		self.soundpack_box.Add(self.soundpackslist, 0, wx.ALL, 10)
		dirs = os.listdir("sounds")
		for i in range(0,len(dirs)):
			self.soundpackslist.Insert(dirs[i],self.soundpackslist.GetCount())
			if twitter.soundpack==dirs[i]:
				self.sp=dirs[i]
				self.soundpackslist.SetSelection(i)
		self.text_label = wx.StaticText(self.panel, -1, "Tweet Footer (Optional)")
		self.footer = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE)
		self.main_box.Add(self.footer, 0, wx.ALL, 10)
		self.footer.AppendText(config.appconfig['general']['footer'])
		self.footer.SetMaxLength(140)
		self.ok = wx.Button(self.panel, wx.ID_OK, "&OK")
		self.ok.Bind(wx.EVT_BUTTON, self.OnOK)
		self.main_box.Add(self.ok, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CLOSE, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def on_soundpacks_list_change(self, event):
		dir(event)
		self.sp=event.GetString()
	def OnOK(self, event):
		config.appconfig['general']['soundpack']=self.sp
		config.appconfig['general']['footer']=self.footer.GetValue()
		config.appconfig.write()
		twitter.soundpack=self.sp
		twitter.footer=config.appconfig['general']['footer']
		self.Destroy()
	def OnClose(self, event):
		self.Destroy()