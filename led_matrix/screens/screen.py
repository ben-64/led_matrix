#!/usr/bin/env python

import sys
import math
from threading import RLock
from led_matrix.fonts.adafruit import AdaFruit


class Screen(object):
    DEFAULT_COLOR = 0
    def __init__(self,width=32,height=8,x=0,y=0,parent=None):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.parent = parent
        self.render_lock = RLock()
        if not self.parent:
            self.buf = [self.DEFAULT_COLOR]*self.height*self.width

    def get_buf(self):
        if self.parent:
            return self.parent.get_buf()
        else:
            return self.buf

    def get_real_height(self):
        if self.parent:
            return self.parent.get_real_height()
        else:
            return self.height

    def get_real_width(self):
        if self.parent:
            return self.parent.get_real_width()
        else:
            return self.width

    def __getitem__(self,i):
        x,y = i[0]+self.x,i[1]+self.y
        return self.get_buf()[self.compute_index(x,y)]

    def __setitem__(self,i,v):
        if i[0] >= self.width or i[0] < 0 or i[1] >= self.height or i[1] < 0:
            return
        x,y = i[0]+self.x,i[1]+self.y
        self.get_buf()[self.compute_index(x,y)] = v
        if self.parent:
            self.parent.set_pixel(x,y,v)
        else:
            self.set_pixel(x,y,v)

    def compute_index(self,i,j):
        if i%2 == 0:
            return i*self.get_real_height()+j
        else:
            return i*self.get_real_height()+(self.get_real_height()-j-1)

    def from_iso_index(self,index):
        x = index%self.width
        y = int(index/self.width)
        return self.compute_index(x,y)

    def set_pixel(self,x,y,color):
        pass

    def pixel(self,x,y,color=None):
        if color is not None:
            self[(x,y)] = color
        else:
            return self[(x,y)]

    def fill(self, color):
        """Fill the entire FrameBuffer with the specified color."""
        self.fill_rect(0, 0, self.width, self.height, color)

    def clear(self):
        self.fill(self.DEFAULT_COLOR)

    def fill_rect(self, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior."""
        if width < 1 or height < 1 or (x + width) <= 0 or (y + height) <= 0 or y >= self.height \
                or x >= self.width:
            return
        x_end = min(self.width, x + width)
        y_end = min(self.height, y + height)
        x = max(x, 0)
        y = max(y, 0)
        for i in range(x,x_end):
            for j in range(y,y_end):
                self[(i,j)] = color

    def hline(self, x, y, width, color):
        """Draw a horizontal line up to a given length."""
        self.fill_rect(x, y, width, 1, color)

    def vline(self, x, y, height, color):
        """Draw a vertical line up to a given length."""
        self.fill_rect(x, y, 1, height, color)

    def rect(self, x, y, width, height, color):
        """Draw a rectangle at the given location, size and color. The ```rect``` method draws only
        a 1 pixel outline."""
        # pylint: disable=too-many-arguments
        self.fill_rect(x, y, width, 1, color)
        self.fill_rect(x, y + height-1, width, 1, color)
        self.fill_rect(x, y, 1, height, color)
        self.fill_rect(x + width - 1, y, 1, height, color)

    def line(self, x_0, y_0, x_1, y_1, color):
        # pylint: disable=too-many-arguments
        """Bresenham's line algorithm"""
        d_x = abs(x_1 - x_0)
        d_y = abs(y_1 - y_0)
        x, y = x_0, y_0
        s_x = -1 if x_0 > x_1 else 1
        s_y = -1 if y_0 > y_1 else 1
        if d_x > d_y:
            err = d_x / 2.0
            while x != x_1:
                self[(x,y)] = color
                err -= d_y
                if err < 0:
                    y += s_y
                    err += d_x
                x += s_x
        else:
            err = d_y / 2.0
            while y != y_1:
                self[(x, y)] = color
                err -= d_x
                if err < 0:
                    x += s_x
                    err += d_y
                y += s_y
        self[(x, y)] = color

    def blit(self):
        """blit is not yet implemented"""
        raise NotImplementedError()

    def scroll(self, delta_x, delta_y, modulo=False):
        """shifts framebuf in x and y direction"""

        if delta_x < 0:
            shift_x = 0
            xend = self.width + delta_x
            dt_x = 1
        else:
            shift_x = self.width - 1
            xend = delta_x - 1
            dt_x = -1
        if delta_y < 0:
            y = 0
            yend = self.height + delta_y
            dt_y = 1
        else:
            y = self.height - 1
            yend = delta_y - 1
            dt_y = -1

        # Data containing border information that will be loosed during scroll
        size = 0
        if delta_x != 0:
            size += abs(delta_x)*self.height
        if delta_y != 0:
            size += abs(delta_x)*self.width

        if not modulo:
            backup = [self.DEFAULT_COLOR]*size
        else:
            x_backup = []
            if delta_x < 0:
                for i in range(abs(delta_x)):
                    bck = []
                    for j in range(self.height):
                        bck.append(self[(i,j)])
                    x_backup = x_backup + bck[-delta_y:] + bck[:-delta_y]
            elif delta_x > 0:
                for i in range(delta_x):
                    bck = []
                    for j in range(self.height):
                        bck.append(self[(self.width-delta_x+i,j)])
                    x_backup = x_backup + bck[-delta_y:] + bck[:-delta_y]

            y_backup = []
            if delta_y < 0:
                for j in range(abs(delta_y)):
                    bck = []
                    for i in range(self.width):
                        bck.append(self[(i,j)])
                    y_backup = y_backup + bck[-delta_x:] + bck[:-delta_x]

            elif delta_y > 0:
                for j in range(delta_y):
                    bck = []
                    for i in range(self.width):
                        bck.append(self[(i,self.height-delta_y+j)])
                    y_backup = y_backup + bck[-delta_x:] + bck[:-delta_x]

            backup = x_backup + y_backup

        while y != yend:
            x = shift_x
            while x != xend:
                self[(x, y)] = self[(x-delta_x,y-delta_y)]
                x += dt_x
            y += dt_y

        if delta_x < 0:
            for i in range(abs(delta_x)):
                for j in range(self.height):
                    self[(self.width-abs(delta_x)+i,j)] = backup[i*self.height+j]
        elif delta_x > 0:
            for i in range(delta_x):
                for j in range(self.height):
                    self[(i,j)] = backup[i*self.height+j]

        if delta_y < 0:
            for j in range(abs(delta_y)):
                for i in range(self.width):
                    self[(i,self.height-abs(delta_y)+j)] = backup[abs(delta_x)*self.height+i+j*self.width]
        elif delta_y > 0:
            for j in range(delta_y):
                for i in range(self.width):
                    self[(i,j)] = backup[abs(delta_x)*self.height+i+j*self.width]


    def text(self, string, x, y, color, font=AdaFruit()):
        w = font.WIDTH
        for i, char in enumerate(string):
            font.draw_char(char=char,x=x + (i * (w+font.space)),y=y,framebuffer=self,color=color)

    def vcenter_text(self,text,color,x=0,font=AdaFruit()):
        text_width = font.width(text)
        y = int((self.height - font.HEIGHT)/2)
        self.text(text,x,y,color,font)

    def hcenter_text(self,text,color,y=0,font=AdaFruit()):
        text_width = font.width(text)
        x = int((self.width - font.width(text))/2)
        self.text(text,x,y,color,font)

    def center_text(self,text,color,font=AdaFruit()):
        text_width = font.width(text)
        x = int((self.width - font.width(text))/2)
        y = int((self.height - font.HEIGHT)/2)
        self.text(text,x,y,color,font)

    def image(self,img,sx=0,sy=0):
        for i in range(img.width):
            for j in range(img.height):
                self[(sx+i,sy+j)] = img[i,j]

    def extract_screen(self,x,y,width,height):
        return Screen(width,height,x,y,self)

    # def image(self, img):
    #     """Set buffer to value of Python Imaging Library image.  The image should
    #     be in 1 bit mode and a size equal to the display size."""
    #     if img.mode != '1':
    #         raise ValueError('Image must be in mode 1.')
    #     imwidth, imheight = img.size
    #     if imwidth != self.width or imheight != self.height:
    #         raise ValueError('Image must be same dimensions as display ({0}x{1}).' \
    #             .format(self.width, self.height))
    #     # Grab all the pixels from the image, faster than getpixel.
    #     pixels = img.load()
    #     # Iterate through the pixels
    #     for x in range(self.width):       # yes this double loop is slow,
    #         for y in range(self.height):  #  but these displays are small!
    #             self[(x, y)] = pixels[(x, y)]

    def stop(self):
        pass

    def colorwipe(self):
        pass

    def render(self):
        if self.parent:
            self.parent.render()
        else:
            self.render_lock.acquire()
            self.raw_render()
            self.render_lock.release()


    def print_index(self,real=True):
        f = self.compute_index if real else lambda x,y:y*self.width+x
        for j in range(self.height):
            for i in range(self.width):
                index = f(i,j)
                sys.stdout.write("%03u " % index)
            print("")
            sys.stdout.flush()
