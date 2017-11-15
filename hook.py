from gpiozero import Button

class Hook:
	def __init__(self,gpio,phone):
		self.input=Button(gpio)
		self.phone=phone
		self.input.when_pressed=self._lower
		self.input.when_released=self._raise
	def _raise(self):
		self.phone.trans(self.phone.raise_hook)
	def _lower(self):
		self.phone.trans(self.phone.lower_hook)
