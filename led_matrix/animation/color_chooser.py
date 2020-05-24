#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct

from led_matrix.animation.network_app import NetworkApplication
from led_matrix.fonts.font4x5 import Font4x5


class ColorChooser(NetworkApplication):
    def print_color(self,value):
        self.screen.clear()
        self.screen.center_text("%02X %02X %02X" % (value>>16,(value>>8)&0xFF,value&0xFF),value,font=Font4x5(space=0))
        self.screen.render()

    def on_receive(self,data):
        value = struct.unpack("<I",data)[0]
        self.print_color(value)

    def update(self):
        pass
