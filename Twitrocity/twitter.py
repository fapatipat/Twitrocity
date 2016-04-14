import collections
import timeline
import sound
import timestring
import datetime
import time
import audio_player
import speak
from threading import Thread
from httplib import HTTPConnection
from urlparse import urlparse
import twishort
import re
import gui
from gui import ask
import tweepy
import webbrowser
import config
import wx

snd=sound.sound()
timelines=collections.OrderedDict()
timelines['home']=timeline.timeline()
timelines['replies']=timeline.timeline()
timelines['messages']=timeline.timeline()
timelines['favorites']=timeline.timeline()
timelines['events']=timeline.timeline()
streaming=0
player=audio_player.URLStream()
tw1="W48NhXLuPeP66yvcXXurhQPY6"
tw2="jST5JRY7KK8tjyxEm6QcpIWrHrMWeHXqyNPsK5w0ohYd9L7kHu"
url_re = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))")
url_re2 = re.compile("(?:\w+://|www\.)[^ ,.?!#%=+][^ ]*")
bad_chars = "'\\.,[](){}:;\""
api=None
listener=None
screenname=""
def Setup():
	global soundpack
	soundpack=config.appconfig['general']['soundpack']
	streaming=0
	global footer
	footer=config.appconfig['general']['footer']
	auth=tweepy.OAuthHandler(tw1, tw2)
	if config.appconfig["general"]["TWKey"]=="" or config.appconfig["general"]["TWSecret"]=="":
		webbrowser.open(auth.get_authorization_url())
		verifier = ask.ask(message='Enter pin:')
		auth.get_access_token(verifier)
		config.appconfig["general"]["TWKey"]=auth.access_token
		config.appconfig["general"]["TWSecret"]=auth.access_token_secret
		config.appconfig.write()
	else:
		auth.set_access_token(config.appconfig["general"]["TWKey"], config.appconfig["general"]["TWSecret"])
	global api
	api = tweepy.API(auth)
	global listener
	global listener2
	listener=StreamListener()
	listener2=ReplyListener()
	global screenname
	m=api.me()
	screenname=m.screen_name
	global Stream
	global Stream2
	Stream = tweepy.Stream(auth = api.auth, listener=listener)
	Stream2 = tweepy.Stream(auth = api.auth, listener=listener2)
	snd.play("welcome")
	gui.interface.spawn()

def backfill():
	t = Thread(target=bf1)
	t.start()
	t2 = Thread(target=bf2)
	t2.start()
	t3 = Thread(target=bf3)
	t3.start()
	t4 = Thread(target=bf4)
	t4.start()
def Tweet(text,id):
	if id!="":
		api.update_status(text,id)
	else:
		api.update_status(text)
	snd.play("sendtweet")
def Retweet(id):
	api.retweet(id)
	snd.play("sendtweet")
def Delete(id):
	api.destroy_status(id)
def Favorite(id):
	api.create_favorite(id)
def Unfavorite(id):
	api.destroy_favorite(id)
def Follow(status):
	api.create_friendship(status)
def Unfollow(status):
	api.destroy_friendship(status)
def Block(status):
	api.create_block(status)
def Unblock(status):
	api.destroy_block(status)
class StreamListener(tweepy.StreamListener):
	def on_disconnect(self):
		streaming=0
	def on_status(self, status):
		status.text=parse(status.text,status)
		add_timeline_item("home",status)
		snd.play("tweet")

	def on_event(self, status):
		add_timeline_item("events",status)
		snd.play("event")

	def on_direct_message(self, status):
		status.direct_message.author=status.direct_message.sender
		status.direct_message.text=parse(status.direct_message.text)
		speak.speak("Message from "+status.direct_message.author['name']+": "+status.direct_message.text)
		snd.play("dm")
		add_timeline_item("messages",status.direct_message)
class ReplyListener(tweepy.StreamListener):
	def on_status(self, status):
		status.text=parse(status.text)
		speak.speak("Reply from "+status.author.name+": "+status.text)
		add_timeline_item("replies",status)
		snd.play("reply")

def find_urls_in_text(text):
 return [s.strip(bad_chars) for s in url_re2.findall(text)]
def unshorten(url):
 working = urlparse(url)
 if not working.netloc:
  raise TypeError, "Unable to parse URL."
 con = HTTPConnection(working.netloc)
 con.connect()
 con.request('GET', working.path)
 resp = con.getresponse()
 con.close()
 return resp.getheader('location')

def parse(text,status=""):
	try:
		if status!=None and status!="" and status.quoted_status:
			new=" Quoting "+status.quoted_status.author.name+" (@"+status.quoted_status.author.screen_name+": "+status.quoted_status.text
			text+=new
			original=""
	except:
		pass
	try:
		if status!=None and status!="" and status.retweeted_status:
			text="retweeted "+status.retweeted_status.author.name+" (@"+status.retweeted_status.author.screen_name+": "+status.retweeted_status.text
	except:
		pass
	urls=find_urls_in_text(text)
	for i in range(0,len(urls)):
		original=urls[i]
		try:
			new=unshorten(urls[i])
		except:
			new=original
		if new!=None and "twishort.com" in new:
			text=twishort.get_full_text(twishort.get_twishort_uri(new))
		if new!=None and "/photo/" in new:
			new="Contains photo"
		if new!=None and "/status/" in new and "twitter.com" in new:
			new=""
		if new!=None and "/statuses/" in new and "twitter.com" in new:
			new=""
		try:
			text=text.replace(original,new)
		except:
			text=text

	return text
def bf1(id=None):
	if id!=None:
		bft=api.home_timeline(count=100,since_id=id)
	else:
		bft=api.home_timeline(count=100)
		i2=len(bft)-1
		bft.reverse()
	for i in range(len(bft)):
		status=bft[i]
		status.text=parse(status.text,status)
		add_timeline_item("home",status,False)
	timelines['home'].make_ready("home")
def bf2(id=None):
	if id!=None:
		bft=api.search(count=100,q="@"+screenname,since_id=id)
	else:
		bft=api.search(count=100,q="@"+screenname)
		bft.reverse()
	for i in range(len(bft)):
		status=bft[i]
		status.text=parse(status.text)
		add_timeline_item("replies",status,False)
	timelines['replies'].make_ready("replies")
def bf3():
	bft=api.favorites(count=200,q="@"+screenname)
	bft.reverse()
	for i in range(len(bft)):
		status=bft[i]
		status.text=parse(status.text)
		add_timeline_item("favorites",status,False)
	timelines['favorites'].make_ready("favorites")
def bf4():
	bft=api.direct_messages(count=100,full_text=True)
	bft.reverse()
	for i in range(len(bft)):
		status=bft[i]
		status.text=parse(status.text)
		add_timeline_item("messages",status,False)
	timelines['messages'].make_ready("messages")
def check_streams():
	streaming=reconnect_streams(0)
def UpdateProfile(name,url,location,description):
	api.update_profile(name,url,location,description)
def exit():
	listener.Disconnect()
	listener2.Disconnect()
def Quote(status,text):
	a=api.get_status(status)
	text+=" https://twitter.com/"+a.author.screen_name+"/status/"+str(status)
	Tweet(text,status)
	snd.play("sendtweet")
def Delete(status):
	api.destroy_status(status)
def play_audio(text):
	player.stop_audio()
	try:
		url=find_urls_in_text(text)
		player.play(url[0])
	except:
		try:
			player.play(url[0])
		except:
			speak.speak("Error: Unable to play")
def stop_audio():
	player.stop_audio()
def pause_audio():
	if player.stream.is_paused==False:
		player.stream.pause()
	else:
		player.stream.play()
def volume_down():
		if player.stream.volume<=0.0:
			speak.speak("Muted")
		else:
			player.stream.volume-=0.05
		speak.speak("Volume is now "+str(round(player.stream.volume,2)))
def svolume_down():
		if config.appconfig['general']['soundvol']<=0.0:
			speak.speak("Muted")
		else:
			config.appconfig['general']['soundvol']-=0.05
		speak.speak("Sound Volume is now "+str(round(config.appconfig['general']['soundvol'],2)))
		appconfig.write()
def svolume_up():
		if config.appconfig['general']['soundvol']>=1.0:
			speak.speak("Full")
		else:
			config.appconfig['general']['soundvol']+=0.05
		speak.speak("Sound Volume is now "+str(round(config.appconfig['general']['soundvol'],2)))
		appconfig.write()
def volume_up():
		if player.stream.volume>=1.0:
			speak.speak("Full")
		else:
			player.stream.volume+=0.05
		speak.speak("Volume is now "+str(round(player.stream.volume,2)))
def parse_date(date):
	ti=datetime.datetime.now()
	tz=time.altzone
	try:
		date+=datetime.timedelta(seconds=0-tz)
	except:
		pass
	returnstring=""

	try:
		if date.year==ti.year:
			if date.day==ti.day and date.month==ti.month:
				returnstring=""
			else:
				returnstring=date.strftime("%m/%d/%Y, ")
		else:
			returnstring=date.strftime("%m/%d/%Y, ")

		if returnstring!="":
			returnstring+=date.strftime("%I:%M:%S %p")
		else:
			returnstring=date.strftime("%I:%M:%S %p")
	except:
		pass
	return returnstring
def delete_item(list, index):
	if list==tweets:
		gui.interface.delete_tweet(index)
		tweets.pop(index)
	if list==replies:
		gui.interface.delete_reply(index)
		replies.pop(index)
	if list==favs:
		gui.interface.delete_fav(index)
		favs.pop(index)
def find_users_in_tweet(status):
	new="@"+status.author.screen_name+" "
	try:
		if status!=None and status!="" and status.quoted_status:
			new+="@"+status.quoted_status.author.screen_name+" "
	except:
		pass
	try:
		if status!=None and status!="" and status.retweeted_status:
			new+="@"+status.retweeted_status.author.screen_name+" "
	except:
		pass
	weew=status.text.split(" ")
	for i in range(0,len(weew)):
		if "@" in weew[i] and weew[i]!="@"+screenname:
			new+=weew[i]+" "
	return new
def reconnect_streams(pull=1,streaming=streaming):
	if streaming==0:
		if pull==1:
			status=timelines['home'].statuses[len(timelines['home'].statuses)-2]
			bf1(status.id)
			status=timelines['replies'].statuses[len(timelines['replies'].statuses)-2]
			bf2(status.id)
		try:
			Stream.userstream("with=following",async=True)
			Stream2.filter(track=["@"+screenname],async=True)
		except:
			pass

		streaming=1
		snd.play("ready")
def add_timeline_item(n,item, streaming=True):
	for i in timelines.keys():
		if i==n:
			if timelines[i].ready==True and streaming==False or timelines[i].ready==False and streaming==False or timelines[i].ready==True and streaming==True:
				timelines[i].statuses.append(item)
			elif timelines[i].ready==False and streaming==True:
				timelines[i].pending.append(item)
			if timelines[i].ready==True and streaming==False or timelines[i].ready==False and streaming==False or timelines[i].ready==True and streaming==True:
				if n!="messages":
					gui.interface.add_to_list(n,item.author.name+": "+item.text+"; "+parse_date(item.created_at)+"; from "+item.source)
				else:
					try:
						gui.interface.add_to_list(n,item.author.name+": "+item.text+"; "+parse_date(item.created_at))
					except:
						gui.interface.add_to_list(n,item.author['name']+": "+item.text+"; "+parse_date(item.created_at))
						pass

			return