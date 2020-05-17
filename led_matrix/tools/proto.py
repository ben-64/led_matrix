#!/usr/bin/env python3

import sys
import socket
import struct


class Protocol(object):
    def __init__(self):
        self.buffer = []

    def add(self,button,color,delay=0):
        self.buffer.append((button,color,delay))

    def get(self,data,sz):
        pass

    def commit(self):
        res = self.generate()
        self.buffer = []
        return res


class BinaryProtocol(Protocol):
    def generate(self):
        res = b""
        for button,color,delay in self.buffer:
            res += struct.pack("<BIB",button,color,delay)
        return res

    def get(self,data):
        res = []
        fmt = "<BIB"
        sz = struct.calcsize(fmt)
        offset = len(res)*sz
        while offset != len(data):
            info = struct.unpack_from(fmt,data,offset)
            res.append(info)
            offset = len(res)*sz
        return res


class UDPClient(object):
    def __init__(self,ip,port=64241,proto=BinaryProtocol()):
        self.addr = (ip,port)
        self.proto = BinaryProtocol()
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def init(self):
        pass

    def add(self,led,color):
        self.proto.add(led,color)

    def send(self):
        data = self.proto.commit()
        if len(data) > 0:
            self.sock.sendto(struct.pack("<I",len(data)),self.addr)
            for i in range(0,len(data),1400):
                self.sock.sendto(data[i:i+1400],self.addr)


class UDPServer(object):
    def __init__(self,port=64242,proto=BinaryProtocol()):
        self.port = port
        self.proto = proto
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def init(self):
        self.sock.bind(("0.0.0.0",self.port))

    def raw_recv(self):
        data,self.addr = self.sock.recvfrom(4096)
        return data

    def recv(self):
        data = b""
        
        l = struct.unpack('<I',self.raw_recv())[0]

        while len(data) != l:
            d = self.raw_recv()
            data += d


class TCPClient(object):
    def __init__(self,ip,port=64241,proto=BinaryProtocol()):
        self.addr = (ip,port)
        self.proto = BinaryProtocol()
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def init(self):
        self.sock.connect(self.addr)

    def add(self,led,color):
        self.proto.add(led,color)

    def send(self):
        data = self.proto.commit()
        if len(data) > 0:
            self.sock.send(struct.pack("<I",len(data)))
            self.sock.send(data)


class TCPServer(object):
    def __init__(self,port=64242,proto=BinaryProtocol()):
        self.port = port
        self.proto = proto
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.csock = None

    def init(self):
        self.sock.bind(("0.0.0.0",self.port))
        self.sock.listen(1)

    def raw_recv(self,sz):
        out = False
        while True:
            try:
                if self.csock == None:
                    self.csock,addr = self.sock.accept()
                data = self.csock.recv(sz)
                if len(data) > 0:
                    out = True
                else:
                    self.csock = None
            except:
                self.csock = None
            else:
                if out: break
        return data

    def recv(self):
        data = b""
        
        l = struct.unpack('<I',self.raw_recv(4))[0]

        while len(data) != l:
            d = self.raw_recv(l-len(data))
            data += d

        return self.proto.get(data)
