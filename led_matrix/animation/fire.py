#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import colorsys
from led_matrix.fonts.adafruit import *
from led_matrix.animation.animation import Animation


def hsv2rgb(h,s,v):
    r,g,b = colorsys.hsv_to_rgb(h/360,s/100,v/100)
    return int(round(r*255)),int(round(g*255)),int(round(b*255))


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


class MagicFire(Animation):
    def __init__(self,hue=10,saturation=100,*args,**kargs):
        super().__init__(*args,**kargs)
        self.hue = hue
        self.saturation = saturation
        self.heat = [[0 for x in range(self.screen.width)] for y in range(self.screen.height)] 

    def set_pixel_heat(self,x,y,heat,max_heat=255):
        base_h = self.hue
        s = self.saturation
        v = 100

        h = base_h + ((heat/255)*10)

        if heat < 10 :
            v = 0
        elif heat < 30:
            v = 50
        elif heat < 40:
            v = 60
        elif heat < 60:
            v = 70
        else:
            v = 100
            h = base_h + 20*heat/max_heat

        r,g,b = hsv2rgb(h,s,v)
        color = (r<<16) | (g<<8) | b
        self.screen[(x,y)] = color


    def fire_line(self,cooling,sparkling,line):
        dir = 1

        # Cooldown
        for i in range(0,self.screen.width,dir):
            cooldown = random.randint(0,int(((cooling*10)/20)+2))
            if cooldown > self.heat[line][i]:
                self.heat[line][i] = 0
            else:
                self.heat[line][i] = self.heat[line][i] - cooldown

        propagation_indice_side = 0
        propagation_indice_up = 0
        # Propagation
        for i in range(0,self.screen.width,dir):
            # Side
            if i == 0:
                self.heat[line][i] = (self.heat[line][i] + self.heat[line][i+dir])/(2+propagation_indice_side)
            elif i == self.screen.width-1:
                self.heat[line][i] = (self.heat[line][i] + self.heat[line][i-dir])/(2+propagation_indice_side)
            else:
                self.heat[line][i] = (self.heat[line][i] + self.heat[line][i-dir] + self.heat[line][i+dir])/(3+propagation_indice_side)

            # Upper/Lower
            if line == 0:
                self.heat[line][i] = (self.heat[line][i] + self.heat[line+dir][i])/(2+propagation_indice_up)
            elif line == self.screen.height-1:
                self.heat[line][i] = (self.heat[line][i] + self.heat[line-dir][i])/(2+propagation_indice_up)
            else:
                self.heat[line][i] = (self.heat[line][i] + self.heat[line-dir][i] + self.heat[line+dir][i])/(3+propagation_indice_up)

        # New spark
        if random.randint(0,255) < sparkling:
            x = int(min(7,max(0,random.normalvariate(4,1))))
            heat = self.generate_heat()
            self.heat[line][x] = heat
            
            side_affected = 0
            for i in range(x-side_affected,x+side_affected):
                if i != x and i >=0 and i <self.screen.width:
                    self.heat[line][i] = self.heat[line][i] + int(heat/(abs(x-i)+2))
            for j in range(line-side_affected,line+side_affected):
                if j != line and j >=0 and j <self.screen.height:
                    self.heat[j][x] = self.heat[j][x] + int(heat/(abs(line-j)+2))

        for i in range(0,self.screen.width,dir):
            self.set_pixel_heat(i,line,self.heat[line][i])


    def generate_heat(self):
        #return random.randrange(5,10)
        return random.randint(220,255)

    def run(self):
        base_cooling = 220

        # If it's faster, congestion will occur at network level
        speed_delay = 0.03

        while not self.stop_received:
            self.fire_line(base_cooling+50,0,0);
            self.fire_line(base_cooling+50,0,1);
            self.fire_line(base_cooling+30,0,2);
            self.fire_line(base_cooling+30,10,3);
            self.fire_line(base_cooling+15,30,4);
            self.fire_line(base_cooling+15,40,5);
            self.fire_line(base_cooling+5,80,6);
            self.fire_line(base_cooling+5,80,7);
            self.screen.render()
            time.sleep(speed_delay)
