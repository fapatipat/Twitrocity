import collections
import application
import speak
import webbrowser
import tweet
import wx
import twitter
import ask, details,options,profile
class MainGui(wx.Frame):
	def __init__(self, title):
		wx.Frame.__init__(self, None, title=title, size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.menuBar = wx.MenuBar()
		menu = wx.Menu()
		m_update = menu.Append(-1, "Update profile", "Update Profile")
		self.Bind(wx.EVT_MENU, self.UpdateProfile, m_update)
		m_options = menu.Append(-1, "Options", "Update Profile")
		self.Bind(wx.EVT_MENU, self.Options, m_options)
		m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
		self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
		self.menuBar.Append(menu, "&Application")
		menu = wx.Menu()
		m_tweet = menu.Append(-1, "&Tweet", "Tweet")
		self.Bind(wx.EVT_MENU, self.Tweet, m_tweet)
		m_reply = menu.Append(-1, "&Reply", "Reply")
		self.Bind(wx.EVT_MENU, self.Reply, m_reply)
		m_reply_all = menu.Append(-1, "&Reply to all", "Reply to all")
		self.Bind(wx.EVT_MENU, self.Reply_all, m_reply_all)
		m_message = menu.Append(-1, "&Send message", "Message")
		self.Bind(wx.EVT_MENU, self.Message, m_message)
		m_edit = menu.Append(-1, "&Edit", "Edit")
		self.Bind(wx.EVT_MENU, self.Edit, m_edit)
		m_delete = menu.Append(-1, "&Delete", "Delete")
		self.Bind(wx.EVT_MENU, self.Delete, m_delete)
		m_retweet = menu.Append(-1, "&Retweet", "Retweet")
		self.Bind(wx.EVT_MENU, self.Retweet, m_retweet)
		m_quote = menu.Append(-1, "&Quote", "Quote")
		self.Bind(wx.EVT_MENU, self.Quote, m_quote)
		m_favorite = menu.Append(-1, "&Favorite", "Favorite")
		self.Bind(wx.EVT_MENU, self.Favorite, m_favorite)
		m_unfavorite = menu.Append(-1, "&Unfavorite", "Unfavorite")
		self.Bind(wx.EVT_MENU, self.Unfavorite, m_unfavorite)
		m_open_url = menu.Append(-1, "&Open URL", "Open URL")
		self.Bind(wx.EVT_MENU, self.Open_url, m_open_url)
		m_view = menu.Append(-1, "&View", "View")
		self.Bind(wx.EVT_MENU, self.View, m_view)
		self.menuBar.Append(menu, "&Tweet")
		menu = wx.Menu()
		m_details = menu.Append(-1, "&View user", "View user")
		self.Bind(wx.EVT_MENU, self.ViewUser, m_details)
		m_follow = menu.Append(-1, "&Follow", "Follow")
		self.Bind(wx.EVT_MENU, self.Follow, m_follow)
		m_unfollow = menu.Append(-1, "&Unfollow", "Unfollow")
		self.Bind(wx.EVT_MENU, self.Unfollow, m_unfollow)
		m_block = menu.Append(-1, "&Block", "Block")
		self.Bind(wx.EVT_MENU, self.Block, m_block)
		m_unblock = menu.Append(-1, "&Unblock", "Unblock")
		self.Bind(wx.EVT_MENU, self.Unblock, m_unblock)
		self.menuBar.Append(menu, "&User")
		menu = wx.Menu()
		m_play = menu.Append(-1, "&Play audio", "Play")
		self.Bind(wx.EVT_MENU, self.Play, m_play)
		m_pause = menu.Append(-1, "&Pause audio", "Pause")
		self.Bind(wx.EVT_MENU, self.Pause, m_pause)
		m_stop = menu.Append(-1, "&Stop audio", "Stop")
		self.Bind(wx.EVT_MENU, self.Stop, m_stop)
		m_volume_up = menu.Append(-1, "&Volume Up", "Up")
		self.Bind(wx.EVT_MENU, self.Volume_up, m_volume_up)
		m_volume_down = menu.Append(-1, "&Volume Down", "Down")
		self.Bind(wx.EVT_MENU, self.Volume_down, m_volume_down)
		m_svolume_up = menu.Append(-1, "&Sounds Volume Up", "Up")
		self.Bind(wx.EVT_MENU, self.SVolume_up, m_svolume_up)
		m_svolume_down = menu.Append(-1, "&Sounds Volume Down", "Up")
		self.Bind(wx.EVT_MENU, self.SVolume_down, m_svolume_down)
		self.menuBar.Append(menu, "&Audio")
		self.SetMenuBar(self.menuBar)
		accel=[]
		accel.append((wx.ACCEL_CTRL, ord('R'), m_reply.GetId()))
		accel.append((wx.ACCEL_CTRL, ord('T'), m_tweet.GetId()))
		accel.append((wx.ACCEL_CTRL, ord('D'), m_message.GetId()))
		accel.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('R'), m_reply_all.GetId()))
		accel.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('T'), m_retweet.GetId()))
		accel.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('Q'), m_quote.GetId()))
		accel.append((wx.ACCEL_CTRL, ord('E'), m_edit.GetId()))
		accel.append((wx.ACCEL_CTRL, ord('L'), m_follow.GetId()))
		accel.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('L'), m_unfollow.GetId()))
		accel.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('V'), m_view.GetId()))
		accel.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('U'), m_details.GetId()))
		accel.append((wx.ACCEL_CTRL, wx.WXK_RETURN, m_play.GetId()))
		accel.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, wx.WXK_RETURN, m_stop.GetId()))
		accel.append((wx.ACCEL_NORMAL, wx.WXK_F5, m_volume_down.GetId()))
		accel.append((wx.ACCEL_NORMAL, wx.WXK_F6, m_volume_up.GetId()))
		accel.append((wx.ACCEL_CTRL, wx.WXK_UP, m_svolume_up.GetId()))
		accel.append((wx.ACCEL_CTRL, wx.WXK_DOWN, m_svolume_down.GetId()))
		accel.append((wx.ACCEL_SHIFT, wx.WXK_RETURN, m_pause.GetId()))
		accel.append((wx.ACCEL_NORMAL, wx.WXK_RETURN, m_open_url.GetId()))
		accel_tbl=wx.AcceleratorTable(accel)
		self.SetAcceleratorTable(accel_tbl)
		self.panel.Layout()
	def on_list_change(self, event):
		dir(event)
	def Options(self, event):
		opt=options.OptionsGui()
		opt.Show()
	def Tweet(self, event):
		twindow=tweet.TweetGui(twitter.footer)
		twindow.Show()
	def Edit(self, event):
		control = self.get_focused_status()
		twindow=tweet.TweetGui(control.text,control.id,1)
		twindow.Show()
	def Play(self, event):
		control = self.get_focused_status()
		twitter.play_audio(control.text)
	def Stop(self,event):
		twitter.stop_audio()

	def Volume_up(self,event):
		twitter.volume_up()

	def SVolume_up(self,event):
		twitter.svolume_up()
	def Volume_down(self,event):
		twitter.volume_down()

	def SVolume_down(self,event):
		twitter.svolume_down()
	def Pause(self,event):
		twitter.pause_audio()

	def Reply(self, event):
		control = self.get_focused_status()
		try:
			twindow=tweet.TweetGui("@"+control.author.screen_name+" ",control.id)

		except:
			twindow=tweet.TweetGui("@"+control.author.screen_name+" ",control.id)
			pass
		twindow.Show()

	def Reconnect(self, event):
		twitter.reconnect_streams()

	def Update_lists(self, event):
		twitter.update_lists()

	def Reply_all(self, event):
		control = self.get_focused_status()
		inreply=twitter.find_users_in_tweet(control)
		id=control.id
		twindow=tweet.TweetGui(inreply,id)

	def Open_url(self, event):
		text=self.find_text()
		url=twitter.find_urls_in_text(text)
		if len(url)>0:
			webbrowser.open(url[0])
		else:
			speak.speak("No URL")
	def Message(self, event):
		control = self.get_focused_status()
		try:
			inreply=control.author.screen_name
		except:
			inreply=control.author['screen_name']
			pass
		twindow=tweet.DMGui(inreply)
		twindow.Show()

	def ViewUser(self, event):
		inreply=ask.ask(message="View who's user details?",default_value=self.get_user())
		status=twitter.api.get_user(inreply)

		if status.location==None:
			status.location="None"
		if status.description==None:
			status.description="None"
		if status.url==None:
			status.url="None"

		twind=details.DetailsGui("Screen name: "+status.screen_name+"\nName: "+status.name+"\nLocation: "+status.location+"\nUser ID: "+status.id_str+"\nFriends: "+str(status.friends_count)+"\nFollowers: "+str(status.followers_count)+"\nTweets: "+str(status.statuses_count)+"\nFavorites: "+str(status.favourites_count)+"\nIn "+str(status.listed_count)+" lists\nProtected: "+str(status.protected)+"\nVerified: "+str(status.verified)+"\nDescription: "+status.description+"\nNotifications enabled: "+str(status.notifications)+"\nLanguage: "+status.lang+"\nURL: "+status.url+"\nCreation date: "+str(status.created_at)+"\nTime zone: "+status.time_zone,inreply)
		twind.Show()
	def get_user(self):
		control = self.get_focused_status()
		try:
			inreply=control.author.screen_name
		except:
			inreply=control.author['screen_name']
			pass

		return inreply

	def Follow(self, event):
		twindow=ask.ask(message="Follow who?",default_value=self.get_user())
		status=twitter.Follow(twindow)

	def Unfollow(self, event):
		twindow=ask.ask(message="Unfollow who?",default_value=self.get_user())
		status=twitter.Unfollow(twindow)

	def Block(self, event):
		twindow=ask.ask(message="Block who?",default_value=self.get_user())
		status=twitter.Block(twindow)

	def Unblock(self, event):
		twindow=ask.ask(message="Unblock who?",default_value=self.get_user())
		status=twitter.Unblock(twindow)

	def Delete(self, event):
		status=self.find_id()
		twitter.Delete(status)

	def Retweet(self, event):
		control = self.get_focused_status()
		id=control.id
		twitter.Retweet(id)

	def Quote(self, event):
		control = self.get_focused_status()
		id=control.id
		t=tweet.QuoteGui(id)
		t.Show()
	def find_id(self):
		control = self.get_focused_status()
		return control.id

	def find_text(self):
		control = self.get_focused_status()
		return control.text
	def Favorite(self, event):
		id=self.find_id()
		twitter.Favorite(id)

	def View(self, event):
		id=self.find_text()
		v=tweet.ViewGui(id)
		v.Show()

	def UpdateProfile(self, event):
		v=profile.ProfileGui()
		v.Show()
	def Unfavorite(self, event):
		id=self.find_id()
		twitter.Unfavorite(id)
	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()
		twitter.exit()
	def get_focused_status(self):
		f=self.FindFocus()
		for i in range(len(twitter.timelines.keys())):
			if twitter.timelines[twitter.timelines.keys()[i]].list==f:
				name=twitter.timelines.keys()[i]
				return twitter.timelines[name].statuses[twitter.timelines[name].list.GetSelection()]
def spawn():
	for i in range(len(twitter.timelines.keys())):
		list_label=wx.StaticText(window.panel, -1, twitter.timelines.keys()[i])
		twitter.timelines[twitter.timelines.keys()[i]].list=wx.ListBox(window.panel, -1)
		window.main_box.Add(twitter.timelines[twitter.timelines.keys()[i]].list, 0, wx.ALL, 10)
def add_to_list(name,text):
	twitter.timelines[name].list.Insert(text,twitter.timelines[name].list.GetCount())
global window
window=MainGui(application.name+" V"+application.version)