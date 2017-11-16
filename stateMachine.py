from transitions import Machine,State
from threading import Lock,Timer

from ringer import Ringer
from hook import Hook
from dialplate import Dialplate
from sipClient import SipClient

class Phone(object):
	def __init__(self):
		self.lock=Lock()
		self.ringer=Ringer(5)
		self.hook=Hook(22,self)
		self.sipClient=SipClient(self)
		self.dialplate=Dialplate(17,27,self)
		self.number=""
		self.dialTimer=None
	def start_ringing(self):
		self.ringer.start_ringing()
	def stop_ringing(self):
		self.ringer.stop_ringing()
	def answer(self):
		print("answer")
	def close_call(self):
		print("close call")
	def dial_number(self):
		self.sipClient.call(self.number)
		self.number=""
		print("dialing")
	def cancel_call(self):
		print("canceling")
	def add_digit(self,digit):
		with self.lock:
			if(self.dialTimer):
				self.dialTimer.cancel()
			self.dialTimer=Timer(3,self._dial_timeout)
			self.dialTimer.start()
			self.number=self.number+str(digit)
			print("Dialed number: " + self.number)
	def _dial_timeout(self):
		print("dial timeout")
		self.dialTimer=None
		self.trans(self.dial_timeout)
	def trans(self,tr):
		retn=None
		with self.lock:
			retn=tr()
		print("State: ",self.state)
		return retn
	def iterate(self):
		self.sipClient.iterate()

states=[
	State(name='disconnected'),
	State(name='idle'),
	State(name='dialing'),
	State(name='calling'),
	State(name='phoning'),
	State(name='ringing',on_enter=['start_ringing'],on_exit=['stop_ringing'])
]

transitions=[
	{'trigger':'connect',          'source':'disconnected',   'dest':'idle'},
	{'trigger':'incoming',         'source':'idle',           'dest':'ringing'},
	{'trigger':'raise_hook',       'source':'idle',           'dest':'dialing'},
	{'trigger':'raise_hook',       'source':'ringing',        'dest':'phoning',  'before':'answer'},
	{'trigger':'cancel_incoming',  'source':'ringing',        'dest':'idle'},
	{'trigger':'lower_hook',       'source':'dialing',        'dest':'idle'},
	{'trigger':'dial_timeout',     'source':'dialing',        'dest':'calling',  'before':'dial_number'},
	{'trigger':'outgoing',         'source':'calling',        'dest':'phoning'},
	{'trigger':'lower_hook',       'source':'calling',        'dest':'idle',     'before':'cancel_call'},
	{'trigger':'lower_hook',       'source':'phoning',        'dest':'idle',     'before':'close_call'},
	{'trigger':'call_closed',      'source':'phoning',        'dest':'idle',     'before':'close_call'},
	{'trigger':'disconnect',       'source':'*',              'dest':'disconnected'}
]

p=Phone()
m=Machine(p,states,transitions=transitions,initial='disconnected')
