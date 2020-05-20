#!/usr/bin/env python

import sys
import math
import time
import random
from threading import Thread
from datetime import datetime
import subprocess

from led_matrix.screens.console import Console
from led_matrix.fonts.font4x5 import Font4x5
from led_matrix.fonts.adafruit import AdaFruit


class Application(Thread):
    def __init__(self,screen=Console(),refresh=60,icon=None):
        super().__init__()
        self.screen = screen
        self.refresh = refresh
        self.stop_received = False
        if icon:
            self.icon = icon
        elif hasattr(self,"ICON"):
            self.icon = getattr(self,"ICON")
        else:
            self.icon = None

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

    def set_icon(self,icon=None):
        if not icon: icon = self.icon
        if not icon: return
        self.screen.image(icon)
        self.data_screen = self.screen.extract_screen(icon.width,0,self.screen.width-icon.width,self.screen.height)

    def stop(self):
        self.stop_received = True

    def wait_finished(self):
        self.join()


class SwitchOff(Application):
    def run(self):
        self.screen.clear()
        self.screen.render()


class TextApplication(Application):
    def __init__(self,color=0xFFFFFF,font=Font4x5(space=0),x=0,y=0,center=True,*args,**kargs):
        super().__init__(*args,**kargs)
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.center = center

    def text_screen(self):
        return self.data_screen if hasattr(self,"data_screen") else self.screen

    def print_text(self,text):
        self.text_screen().fill(self.screen.DEFAULT_COLOR)
        if self.center:
            self.text_screen().center_text(text,self.color,font=self.font)
        else:
            self.text_screen().text(text,self.x,self.y,self.color,self.font)
        self.screen.render()


class ScrollText(TextApplication):
    def __init__(self,if_needed=True,speed=0.5,letter_by_letter=True,infinite=False,*args,**kargs):
        super().__init__(*args,**kargs)
        self.letter_by_letter = letter_by_letter
        self.indice_start = 0
        self.indice_end = None
        self.speed = speed
        self.if_needed = if_needed
        self.infinite = infinite

    def set_text(self):
        return "Scrolling text"

    def update(self):
        text = self.set_text()
        if self.font.width(text) > self.text_screen().width:
            self.scroll(text)
        else:
            self.print_text(text)

    def scroll(self,text):
        stop = False
        while not self.stop_received and not stop:
            self.print_text(text[self.indice_start:self.indice_end])
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
                    if not self.infinite:
                        stop = True

            time.sleep(self.speed)


class Date(ScrollText):
    def set_text(self):
        return datetime.now().strftime("%a %d %b")


class Bar(object):
    """ A simple Bar that can be increased or decreased """
    def __init__(self,screen,color=0xFF,bgcolor=0):
        self.screen = screen
        self.color = color
        self.bgcolor = bgcolor

    def update(self,value):
        if value < 0: value = 0
        for i in range(value):
            self.screen[(i,0)] = self.color
        for i in range(value,self.screen.width-1):
            self.screen[(i,0)] = self.bgcolor


class ProgressBar(object):
    def __init__(self,screen,max_value,color=0xFF,bgcolor=0x111111):
        self.screen = screen
        self.color = color
        self.bgcolor = bgcolor
        self.max_value = max_value

    def update(self,value):
        full = int(self.screen.width*value/(self.max_value-1))
        for i in range(self.screen.width):
            color = self.color if i<full else self.bgcolor
            self.screen[(i,0)] = color


class Clock(TextApplication):
    def __init__(self,*args,**kargs):
        super().__init__(refresh=1,*args,**kargs)
        sz_icon = 9
        self.icon_screen = self.screen.extract_screen(0,0,sz_icon,self.screen.height)
        self.time_screen = self.screen.extract_screen(sz_icon,0,self.screen.width-sz_icon,self.screen.height-1)
        self.second_screen = self.screen.extract_screen(sz_icon,7,self.screen.width-sz_icon,1)
        self.bartimer = ProgressBar(self.second_screen,60)

    def set_icon(self):
        for x in range(self.icon_screen.width):
            for y in range(self.icon_screen.height):
                if y == 0: color = 0xFF0000
                else: color = 0xFFFFFF
                self.icon_screen[(x,y)] = color
        day = datetime.now().strftime("%d").lstrip("0")
        self.icon_screen.text(day,color=0,font=Font4x5(0),x=1,y=2)

    def update(self):
        # Time
        self.time_screen.fill(self.screen.DEFAULT_COLOR)
        self.time_screen.center_text(datetime.now().strftime("%H:%M"),color=0xFFFFFF,font=Font4x5(0))

        # Seconds
        nb_seconds = int(datetime.now().strftime("%S"))
        self.bartimer.update(nb_seconds)

        self.screen.render()


class SmallClock(TextApplication):
    ICON = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0xb596, 0x0, 0x0, 0x0, 0x0, 0x0, 0xb596, 0xb596, 0x0]

    def update(self):
        self.print_text(datetime.now().strftime("%H:%M"))


class ExternalCommand(ScrollText):
    def __init__(self,cmd,*args,**kargs):
        super().__init__(*args,**kargs)
        self.cmd = cmd

    def set_text(self):
        return subprocess.check_output(self.cmd,shell=True).decode("utf-8").strip()
        

class Animation(Application):
    pass


