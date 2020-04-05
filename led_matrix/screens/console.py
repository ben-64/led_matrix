#!/usr/bin/env python

import sys
from led_matrix.screens.screen import Screen

try:
    import curses
    has_curses = True
except:
    has_curses = False


class Console(Screen):
    DEFAULT_COLOR = "."

    def render(self):
        for j in range(self.height):
            for i in range(self.width):
                index = self.compute_index(i,j)
                sys.stdout.write("%s" % "#" if self.buf[index] != self.DEFAULT_COLOR and self.buf[index] != 0 else self.DEFAULT_COLOR)
            print("")
        print("")
        sys.stdout.flush()


if has_curses:
    class NcursesConsole(Screen):
        DEFAULT_COLOR = 0xFFFFFF
        CHAR = "#"
        COLOR_MAX_CURSES=1000
        RGB_MAX=255

        def __init__(self,*args,**kargs):
            super().__init__(*args,**kargs)
            self.stdscr = curses.initscr()
            curses.curs_set(0)
            curses.start_color()
            curses.use_default_colors()
            self.init_colors()
            # width+1 to avoid error when writting to the lowest right character
            self.win = curses.newwin(self.height, self.width+1)
            self.fill(self.DEFAULT_COLOR)

        @staticmethod
        def color2rgb(c):
            def adapt(c):
                return int(c/3*NcursesConsole.RGB_MAX)
            return adapt((c>>4)&3),adapt((c>>2)&3),adapt(c&3)

        @staticmethod
        def rgb2color(r,g,b):
            def adapt(c):
                return int(c/NcursesConsole.RGB_MAX*3)
            return adapt(r)<<4 | adapt(g)<<2 | adapt(b)

        @staticmethod
        def rgbcolor2cursescolor(r,g,b):
            f = lambda x:int(x/NcursesConsole.RGB_MAX*NcursesConsole.COLOR_MAX_CURSES)
            return f(r),f(g),f(b)

        def init_colors(self):
            for c in range(255):
                r,g,b = NcursesConsole.rgbcolor2cursescolor(*NcursesConsole.color2rgb(c))
                curses.init_color(c,r,g,b)
                curses.init_pair(c,c,c)

        def color2internal(self,color):
            r = (color & 0xFF0000)>>16
            g = (color & 0xFF00)>>8
            b = color & 0xFF
            return NcursesConsole.rgb2color(r,g,b)

        def set_pixel(self,x,y,color):
            color = self.color2internal(color)
            try:
                self.win.addstr(y, x, self.CHAR, curses.color_pair(color))
            except:
                self.stop()
                raise

        def render(self):
            try:
                self.win.refresh()
            except:
                self.stop()
                raise

        def stop(self):
            curses.curs_set(1)
            curses.endwin()
