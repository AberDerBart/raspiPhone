from gpiozero import DigitalOutputDevice

class Ringer:
	def __init__(self,gpio):
		self.output=DigitalOutputDevice(gpio)
	def start_ringing(self):
		print("start ringing")
		self.output.blink(on_time=1.5,off_time=.5)
	def stop_ringing(self):
		print("stop ringing")
		self.output.off()
