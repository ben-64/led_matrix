#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from led_matrix.animation.animation import Application
from led_matrix.tools.proto import UDPServer

class NetworkAppli(Application):
    def __init__(self,net=UDPServer(),*args,**kargs):
        super().__init__(*args,**kargs)
        self.net = net

    def to_coord(self,index):
        x = index%self.screen.width
        y = int(index/self.screen.width)
        return (x,y)

    def run(self):
        self.net.init()
        while True:
            data = self.net.recv()
            for led,color,delay in data:
                self.screen[self.to_coord(led)] = color
            self.screen.render()
