#!/usr/bin/python
from gpiozero import Button
import linphone
import logging

class SipClient:
    core=None
    def __init__(self):
        callbacks={ 
                'registration_state_changed': self.registration_changed,
                'call_state_changed': self.call_changed,
        }

        self.core=linphone.Core.new(callbacks,"phone.conf",None)

    def configure(self):
        addr = self.core.create_address("sip:taubsi78@fritz.box")

        proxy_cfg = self.core.create_proxy_config()
        proxy_cfg.identity_address=addr
        proxy_cfg.server_addr="sip:fritz.box"
        proxy_cfg.register_enabled = True

        self.core.add_proxy_config(proxy_cfg)
        self.core.default_proxy_config=proxy_cfg

        auth=self.core.create_auth_info("taubsi78","taubsi78","aquarium","","","")
        self.core.add_auth_info(auth)
    def registration_changed(self, core, call, state, message):
        print("Registration State: " + str(state) + ":" + message)
    def call_changed(self, core, call, state, message):
        print("Call State:         " + str(state) + ":" + message)
    def iterate(self):
        self.core.iterate()
    def call(self,addr):
        self.core.invite(addr)

def log_handler(level, msg):
        method = getattr(logging, level)
        method(msg)

linphone.set_log_handler(log_handler)
