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

    def concatenate(self,img,empty_val=0,space=1):
        data = []
        diff = abs(self.height - img.height)
        if img.height > self.height:
            for j in range(0,diff):
                for i in range(self.width+space):
                    data.append(empty_val)
                for i in range(img.width):
                    data.append(img[i,j])
            for j in range(self.height):
                for i in range(self.width):
                    data.append(self[i,j])
                for i in range(space):
                    data.append(empty_val)
                for i in range(img.width):
                    data.append(img[i,j+diff])
        else:
            for j in range(0,diff):
                for i in range(self.width):
                    data.append(self[i,j])
                for i in range(space):
                    data.append(empty_val)
                for i in range(img.width):
                    data.append(empty_val)
            for j in range(img.height):
                for i in range(self.width):
                    data.append(self[i,j+diff])
                for i in range(space):
                    data.append(empty_val)
                for i in range(img.width):
                    data.append(img[i,j])
        return Image(data,self.width+img.width+space,max(self.height,img.height))
 

class SquareImage(Image):
    def __init__(self,data):
        side = int(math.sqrt(len(img)))
        super().__init__(data,width=side,height=side)
