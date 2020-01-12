#!/usr/bin/env python

import sys
import math
import time
import random
from threading import Thread
from datetime import datetime

from led_matrix.screen import *
from led_matrix.fonts.font4x5 import Font4x5
from led_matrix.fonts.adafruit import AdaFruit

class Application(Thread):
    def __init__(self,screen=Console(),refresh=60):
        super().__init__()
        self.screen = screen
        self.refresh = refresh
        self.stop_received = False

    def run(self):
        self.set_icon()
        sec = 0
        while not self.stop_received:
            # Just to avoid long waiting threads
            if self.refresh > 1:
                if sec % self.refresh == 0:
                    self.update()
                sec += 1
                time.sleep(1)
            else:
                self.update()
                time.sleep(self.refresh)

    def run_bg(self):
        self.start()

    def update(self):
        raise NotImplementedError()

    def has_icon(self):
        return hasattr(self,"ICON")

    def set_icon(self,icone=None):
        if not icone and not self.has_icon():
            return
        elif not icone:
            icone = self.ICON
        self.screen.image(icone)
        side = int(math.sqrt(len(icone)))
        self.data_screen = self.screen.extract_screen(side,0,self.screen.width-side,self.screen.height)

    def stop(self):
        self.stop_received = True

    def wait_finished(self):
        self.join()

class SwitchOff(Application):
    def run(self):
        self.screen.colorwipe()
        self.screen.render()

class TextApplication(Application):
    def text_screen(self):
        return self.data_screen if hasattr(self,"data_screen") else self.screen

    def print_text(self,text,color=0xFFFFFF,font=Font4x5(),space=0,x=0,y=0,center=True):
        self.text_screen().fill(self.screen.DEFAULT_COLOR)
        if center:
            self.text_screen().center_text(text,color,font=font,space=space)
        else:
            self.text_screen().text(text,x,y,color,font,space)
        self.screen.render()

class ScrollText(TextApplication):
    def __init__(self,speed=0.5,letter_by_letter=True,*args,**kargs):
        super().__init__(*args,**kargs)
        self.letter_by_letter = letter_by_letter
        self.indice_start = 0
        self.indice_end = None
        self.x = 0
        self.font = Font4x5()
        self.speed = speed

    def set_text(self):
        return "Scrolling text"

    def update(self):
        text = self.set_text()

        while not self.stop_received:
            self.print_text(text[self.indice_start:self.indice_end],center=False,x=self.x,font=self.font)
            if not self.letter_by_letter or self.indice_end is None:
                self.indice_start += 1
                if self.indice_start > len(text):
                    self.indice_start = 0
                    if self.indice_end is None:
                        self.indice_end = 1
                        self.x = self.screen.width - self.font.WIDTH
            else:
                self.indice_end += 1
                self.x -= self.font.WIDTH
                if self.x < 0:
                    self.indice_start = 1
                    self.indice_end = None
                    self.x = 0

            time.sleep(self.speed)
            
class Date(ScrollText):
    def set_text(self):
        return datetime.now().strftime("%a %d %b")

class Clock(TextApplication):
    def __init__(self,*args,**kargs):
        super().__init__(refresh=1,*args,**kargs)
        self.icon_screen = self.screen.extract_screen(0,0,8,self.screen.height)
        self.time_screen = self.screen.extract_screen(8,0,self.screen.width-8,self.screen.height-1)
        self.second_screen = self.screen.extract_screen(8,7,self.screen.width-8,1)


    def set_icon(self):
        for x in range(self.icon_screen.width):
            for y in range(self.icon_screen.height):
                if y == 0: color = 0xFF0000
                else: color = 0xFFFFFF
                self.icon_screen[(x,y)] = color
        day = datetime.now().strftime("%d").lstrip("0")
        self.icon_screen.hcenter_text(day,color=0,font=Font4x5(),y=2,space=0)

    def update(self):
        # Time
        self.time_screen.fill(self.screen.DEFAULT_COLOR)
        self.time_screen.center_text(datetime.now().strftime("%H:%M"),color=0xFFFFFF,font=Font4x5(),space=0)

        # Seconds
        nb_seconds = int(datetime.now().strftime("%S"))
        pixel_for_seconds = 20
        step = int((self.second_screen.width-pixel_for_seconds)/2)
        full = int(((pixel_for_seconds+1)*nb_seconds)/60)
        for i in range(pixel_for_seconds):
            color = 0xFF if i<=full else 0x111111
            self.second_screen[(i+step,0)] = color

        self.screen.render()


class SmallClock(TextApplication):
    ICON = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0]

    def update(self):
        self.print_text(datetime.now().strftime("%H:%M"))


class Animation(Application):
    pass


