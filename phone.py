#!/usr/bin/python
from gpiozero import Button
import linphone
import logging

class PhoneInput:
    def __init__(self, gpioTick, gpioDial, gpioHook):
        # init member variables
        self.ticks=0
        self.dialedNumber=""

        # init gio pins
        self.btnHook=Button(gpioHook)
        self.btnTick=Button(gpioTick)
        self.btnDial=Button(gpioDial)

        # init gpio callbacks
        self.btnTick.when_pressed=self.incTicks

        self.btnDial.when_pressed=self.resetTicks
        self.btnDial.when_released=self.addDigit

        self.btnHook.when_pressed=self.hangup
        self.btnHook.when_released=self.call
    def incTicks(self):
        self.ticks=self.ticks+1
    def resetTicks(self):
        self.ticks=0
    def addDigit(self):
        if self.ticks:
            self.dialedNumber+=str(self.ticks%10)
    def hangup(self):
        print("hangup")
        self.dialedNumber=""
    def call(self):
        print(self.dialedNumber)

class PhoneClient:
    core=None
    def __init__(self):
        callbacks={ 
                'global_state_changed': self.global_changed,
                'registration_state_changed': self.registration_changed,
        }

        self.core=linphone.Core.new(callbacks,"phone.conf",None)


        addr = self.core.create_address("sip:taubsi78@fritz.box")

        proxy_cfg = self.core.create_proxy_config()
        proxy_cfg.identity_address=addr
        proxy_cfg.server_addr="sip:fritz.box"
        proxy_cfg.register_enabled = True

        self.core.add_proxy_config(proxy_cfg)
        self.core.default_proxy_config=proxy_cfg

        auth=self.core.create_auth_info("taubsi78","taubsi78","aquarium","","","")
        self.core.add_auth_info(auth)
    def global_changed(self,*args, **kwargs):
        pass
    def registration_changed(core, call, state, message):
        pass

def log(level,msg):
    print(level,msg)

linphone.set_log_handler(log)
i=PhoneInput(17,27,22)
