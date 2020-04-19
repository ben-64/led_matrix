#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import io
from PIL import Image as PILImage

from led_matrix.images.image import Image
from led_matrix.animation.sprite import Sprite

# Use of icons provided by the Awtric project
# https://awtrix.blueforcer.de/icons.html

class AwtrixImage(Sprite):
    URL = "https://awtrix.blueforcer.de/icons"
    
    def __init__(self,icon):
        img = self.load_awtrix_icon(icon)
        super().__init__(img)

    def load_awtrix_icon(self,icon):
        r = requests.get('%s/%u' % (self.URL,icon))
        img = PILImage.open(io.BytesIO(r.content))

        if "loop" in img.info:
            frames = []
            for i in range(img.n_frames):
                img.seek(i)
                f = img.convert("RGB")
                frames.append(self.from_pil(f,int(img.width/8)))
            return frames
        
        img = img.convert("RGB")
        return self.from_pil(img,int(img.width/8))

    def from_pil(self,img,zoom):
        data = []
        for j in range(0,img.height,zoom):
            for i in range(0,img.width,zoom):
                r,g,b = img.getpixel((i,j))
                data.append(r<<16|g<<8|b)
        return Image(data,8,8,color=None)
