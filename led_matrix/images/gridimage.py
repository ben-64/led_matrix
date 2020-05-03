#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from PIL import Image as PILImage

from led_matrix.images.image import Image


_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_img_data(path):
    return os.path.join(_ROOT, 'data', path)


class GridImage(object):
    ALTER = lambda s,r,g,b:(r,g,b)
    """ Class used to manage GRID of images, because I'm a lazy man... """
    def __init__(self,path=None,sx=None,sy=None,space=None,zoom=None,alter=None,side=8):
        self.sx = sx if sx else self.SX
        self.sy = sy if sy else self.SY
        self.space = space if space else self.SPACE
        self.zoom = zoom if zoom else self.ZOOM
        self.path = path if path else self.PATH
        self.alter = alter if alter else self.ALTER
        self.side = side

    def extract_pil_image(self,x,y):
        sx = self.sx + (self.side*self.zoom + self.space) * x
        ex = sx+self.side*self.zoom
        sy = self.sy + (self.side*self.zoom + self.space) * y
        ey = sy+self.side*self.zoom
        box = (sx,sy,ex,ey)
        img = PILImage.open(self.path).convert("RGB")
        return img.crop(box)

    def get_image(self,x,y):
        data = []
        img = self.extract_pil_image(x,y)
        for j in range(0,img.height,self.zoom):
            for i in range(0,img.width,self.zoom):
                r,g,b = img.getpixel((i,j))
                r,g,b = self.ALTER(r,g,b)
                data.append(r<<16|g<<8|b)
        return Image(data,8,8,color=None)


class CHARACTER(GridImage):
    def improve_red(self,r,g,b):
        if r == 255 and b == 77 and g == 0: return 255,0,0
        else: return r,g,b
    SX = 36
    SY = 36
    SPACE = 24
    ZOOM = 6
    ALTER = improve_red
    # https://twitter.com/johanvinet/status/635814153601597441
    PATH = get_img_data("characters.png")

class FOOD(GridImage):
    def improve_red(self,r,g,b):
        if r == 255 and b == 77 and g == 0: return 255,0,0
        else: return r,g,b
    SX = 17
    SY = 21
    SPACE = 16
    ZOOM = 4
    ALTER = improve_red
    # https://twitter.com/JUSTIN_CYR/status/634546317713391616
    PATH = get_img_data("food.png")

class SUPER_HEROES(GridImage):
    def improve_color(self,r,g,b):
        if r==0xff and g==0xc0 and b==0x95: return 0x8F,0x50,0x35
        elif r == 255 and b == 50 and g == 0: return 255,0,0
        else: return r,g,b
    SX = 50
    SY = 50
    SPACE = 16
    ZOOM = 8
    ALTER = improve_color
    # https://www.behance.net/gallery/32551489/8x8-100-superhero-faces-pico8-color-palette
    PATH = get_img_data("super_heroes.png")
