#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
from led_matrix.fonts.adafruit import *
from led_matrix.fonts.font4x5 import *
from led_matrix.animation.animation import TextApplication

class Temperature(TextApplication):
    """ URL is a the domoticz server """

    def __init__(self,url,icon=None,color=0xFFFFFF,*args,**kargs):
        super().__init__(*args,**kargs)
        self.url = url
        self.color = color
        self.icon = icon
        sz = 7
        if self.icon is None:
            self.data_screen = self.screen
        else:
            self.data_screen = self.screen.extract_screen(sz,0,self.screen.width-sz,self.screen.height)
            self.icon_screen = self.screen.extract_screen(0,0,sz,self.screen.height)

    def update(self):
        self.screen.fill(self.screen.DEFAULT_COLOR)
        x = urllib.request.urlopen(self.url)
        j = json.loads(x.read().decode("utf-8"))
        temp = j["result"][0]["Temp"]
        if not self.icon is None:
            self.icon_screen.center_text(self.icon,color=self.color,font=AdaFruit())
        self.data_screen.center_text("%.1f" % temp,color=0xFFFFFF,font=Font4x5(0))
        self.screen.render()
