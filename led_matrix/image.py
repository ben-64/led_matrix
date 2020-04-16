#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class Image(object):
    def __init__(self,data,width,height):
        self.data = data
        self.width = width
        self.height = height

    def __getitem__(self,i):
        return self.data[self.from_coord(i[0],i[1])]

    def display(self):
        for j in range(self.height):
            for i in range(self.width):
                sys.stdout.write("%s" % (str(self[i,j]).ljust(12," "),))
            print()

    def from_coord(self,x,y):
        return y*self.width+x

class SquareImage(Image):
    def __init__(self,data):
        side = int(math.sqrt(len(img)))
        super().__init__(data,width=side,height=side)
