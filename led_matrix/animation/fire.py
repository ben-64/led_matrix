#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from led_matrix.fonts.adafruit import *
from led_matrix.animation.animation import Animation

class Fire(Animation):
    def run(self):
        fire = [[0 for i in range(self.screen.height)] for x in range(self.screen.width)]

        while not self.stop_received:
            for x in range(self.screen.width):
                fire[x][self.screen.height-1] = random.randint(0,0xFFFFFF) & 0x3FF

            for y in range(self.screen.height-1):
                for x in range(self.screen.width):
                    v = fire[(x - 1 + self.screen.width) % self.screen.width][(y + 1) % self.screen.height] + \
                        fire[x][(y + 1) % self.screen.height] + \
                        fire[(x + 1 + self.screen.width) % self.screen.width][(y + 1) % self.screen.height] + \
                        fire[x][(y + 2) % self.screen.height]
                    v = float(v) / 7.5
                    fire[x][y] = int(v)&0xFFFF 

        
            for y in range(self.screen.height):
                for x in range(self.screen.width):
                    if fire[x][y] < 256:
                        self.screen[(x,y)] = (fire[x][y]&0xFF)<<16
                    else:
                        self.screen[(x,y)] = 0xFF0000 | (fire[x][y]-256)<<8 

            self.screen.render()
            time.sleep(0.05)


