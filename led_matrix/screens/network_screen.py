#!/usr/bin/env python

import sys
from led_matrix.screens.screen import Screen
from led_matrix.tools.proto import UDPClient,TCPClient


class NetworkScreen(Screen):
    """ Simulate a screen sending pixel change to the network """
    def __init__(self,dst="127.0.0.1",port=64240,*args,**kargs):
        super().__init__(*args,**kargs)
        self.net = TCPClient(dst,port)
        self.net.init()

    def compute_index(self,x,y):
        return y*self.get_real_width()+x

    def set_pixel(self,x,y,color):
        led = self.compute_index(x,y)
        self.net.add(led,color)

    def raw_render(self):
        self.net.send()
