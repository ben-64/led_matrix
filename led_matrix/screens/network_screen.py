#!/usr/bin/env python

import sys
from led_matrix.screens.screen import Screen
from led_matrix.tools.proto import UDPClient


class NetworkScreen(Screen):
    def __init__(self,net=UDPClient("127.0.0.1",64243),*args,**kargs):
        super().__init__(*args,**kargs)
        self.net = net

    def compute_index(self,x,y):
        return y*self.get_real_width()+x

    def set_pixel(self,x,y,color):
        led = self.compute_index(x,y)
        self.net.add(led,color)

    def render(self):
        self.net.send()
