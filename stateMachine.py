from transitions import Machine,State
from ringer import Ringer

class Phone(object):
	def __init__(self):
		self.ringer=Ringer(5)
	def start_ringing(self):
		self.ringer.start_ringing()
	def stop_ringing(self):
		self.ringer.stop_ringing()
	def answer(self):
		print("answer")
	def close_call(self):
		print("close call")
	def dial_number(self):
		print("dialing")
	def cancel_call(self):
		print("canceling")
		

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
	{'trigger':'disconnect',       'source':'*',              'dest':'disconnected'}
]

p=Phone()
m=Machine(p,states,transitions=transitions,initial='disconnected')
