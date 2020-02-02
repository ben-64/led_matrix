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



# Taken from https://github.com/NiklasFauth/magic-mason-jar/blob/master/mason_fire/mason_fire.ino
class Fire2(Animation):
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        self.heat = [[0 for x in range(self.screen.width)] for y in range(self.screen.height)] 

    def set_pixel_heat(self,x,y,heat):
        c = round((heat/255)*191)

        heatramp = c & 0x3f
        heatramp <<= 2

        if c <= 0x40:  # Coolest
            heatramp <<= 16
        elif c <= 0x80:
            heatramp |= 0xFF00
            heatramp <<= 8
        else:
            heatramp |= 0xFFFF00

        self.screen.set_pixel(x,y,heatramp)
        
    def fire_line(self,cooling,sparkling,speeddelay,line):
        dir = 1

        for i in range(0,self.screen.width,dir):
            cooldown = random.randint(0,int(((cooling*10)/20)+2))
            if cooldown > self.heat[line][i]:
                self.heat[line][i] = 0
            else:
                self.heat[line][i] = self.heat[line][i] - cooldown

        for i in range(self.screen.width-1,2,-dir):
            self.heat[line][i] = (self.heat[line][i-dir] + self.heat[line][i-dir-dir] + self.heat[line][i-dir-dir])/3

        if random.randint(0,255) < sparkling:
            y = random.randint(0,4)
            self.heat[line][y] - random.randint(120,160)

        for i in range(0,self.screen.width,dir):
            self.set_pixel_heat(i,line,self.heat[line][i])

        self.screen.render()
        time.sleep(speeddelay)

    def run(self):
        while not self.stop_received:
            self.fire_line(30,17,0, 0);
            self.fire_line(25,25,0, 1);
            self.fire_line(20,30,0, 2);
            self.fire_line(15,40,0, 3);
            self.fire_line(15,40,0, 4);
            self.fire_line(25,40,0, 5);
            self.fire_line(30,30,0, 6);
            self.fire_line(25,25,0, 7);

