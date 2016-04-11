import config
import twitter
import sound_lib
from sound_lib import output
from sound_lib import stream
class sound():
	handle=0
	def play(self, filename):
		self.handle =stream.FileStream(file="sounds/"+twitter.soundpack+"/"+filename+".ogg")
		self.handle.volume=config.appconfig['general']['soundvol']
		self.handle.looping=False
		self.handle.play()
	def play_wait(self,filename):
		self.handle =stream.FileStream(file="sounds/"+twitter.soundpack+"/"+filename+".ogg")
		self.handle.volume=config.appconfig['general']['soundvol']
		self.handle.looping=False
		self.handle.play_blocking()