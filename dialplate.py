from gpiozero import Button

class Dialplate:
	def __init__(self, gpioTick, gpioDial, phone):
		# init member variables
		self.ticks=0

		self.phone=phone

		# init gio pins
		self.btnTick=Button(gpioTick)
		self.btnDial=Button(gpioDial)

		# init gpio callbacks
		self.btnTick.when_pressed=self._incTicks

		self.btnDial.when_pressed=self._resetTicks
		self.btnDial.when_released=self._sendDigit
	def _incTicks(self):
		self.ticks=self.ticks+1
	def _resetTicks(self):
		self.ticks=0
	def _sendDigit(self):
		if self.ticks:
			self.phone.add_digit(self.ticks%10)
