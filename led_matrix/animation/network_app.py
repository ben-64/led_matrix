#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import select
from threading import Thread

from led_matrix.animation.animation import Application
from led_matrix.tools.proto import UDPServer,TCPServer,DisconnectError


class ProxyScreen(Application):
    """ Virtual screen listening on network and applying colors to another screen """
    def __init__(self,port=64240,*args,**kargs):
        super().__init__(*args,**kargs)
        self.net = TCPServer(port)

    def to_coord(self,index):
        x = index%self.screen.width
        y = int(index/self.screen.width)
        return (x,y)

    def run(self):
        self.net.init()
        while True:
            try:
                data = self.net.recv()
            except DisconnectError:
                self.screen.clear()
            else:
                for led,color,delay in data:
                    self.screen[self.to_coord(led)] = color
            self.screen.render()


class NetworkThread(Thread):
    def __init__(self,callback,port=64241):
        super().__init__()
        self.port = port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.need_stop = False
        self.callback = callback

    def init(self):
        self.sock.bind(("0.0.0.0",self.port))

    def run(self):
        self.init()
        while not self.need_stop:
            ready = select.select([self.sock], [], [], 1)
            if ready[0]:
                data = self.sock.recv(4096)
                self.callback(data)

    def stop(self):
        self.need_stop = True


class NetworkApplication(Application):
    """ Application listening on network """
    def __init__(self,port=64241,*args,**kargs):
        super().__init__(*args,**kargs)
        self.net_thread = NetworkThread(self.on_receive,port)
        self.net_thread.start()

    def stop(self):
        super().stop()
        self.net_thread.stop()

    def on_receive(self,data):
        pass
