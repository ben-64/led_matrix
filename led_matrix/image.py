#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

class Image(object):
    def __init__(self,data,width,height,color={1:0xFFFFFF}):
        self.data = self.load_color(data,color)
        self.width = width
        self.height = height

    def __getitem__(self,i):
        return self.data[self.from_coord(i[0],i[1])]

    def load_color(self,data,color={1:0xFFFFFF}):
        if color is None:
            return data
        elif type(color) is int:
            color = {1:color}
        return [color.get(x,x) for x in data]

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


class ImageStr(Image):
    def __init__(self,s,pattern={"#":1},color={1:0xFFFFFF}):
        data,width,height = self.load_str(s,pattern)
        super().__init__(data,width,height,color)

    def load_str(self,s,replace):
        r = []
        height = 0
        for line in s.splitlines():
            height += 1
            width = len(line)
            for c in line:
                r.append(replace.get(c,0))
        return r,width,height


class StaticImage(ImageStr):
    IMAGE = ""
    DEFAULT_COLOR = {1:0xFFFFFF}
    DEFAULT_PATTERN = {"#":1}
    def __init__(self,pattern=None,color=None):
        color = color if color else self.DEFAULT_COLOR
        pattern = pattern if pattern else self.DEFAULT_PATTERN
        super().__init__(self.IMAGE,pattern,color)

    
