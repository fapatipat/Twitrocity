import twitter
import gui
class timeline(object):
	index=0
	def __init__(self,type=""):
		self.listen=0
		self.f=0
		self.stream=0
		self.ready=False
		self.statuses=[]
		self.type=type
		self.pending=[]
		self.list=None
	def make_ready(self,name):
		self.ready=True
		if len(self.pending)>0:
			for i in range(len(self.pending)):
				self.statuses.append(self.pending[i])
				try:
					gui.interface.add_to_list(name,self.pending[i].author.name+": "+self.pending[i].text+"; "+twitter.parse_date(self.pending[i].created_at)+"; from "+self.pending[i].source)
				except:
					try:
						gui.interface.add_to_list(name,self.pending[i].author.name+": "+self.pending[i].text+"; "+twitter.parse_date(self.pending[i].created_at))
					except:
						gui.interface.add_to_list(name,self.pending[i].author['name']+": "+self.pending[i].text+"; "+twitter.parse_date(self.pending[i].created_at))
						pass
					pass
				self.pending.pop(i)