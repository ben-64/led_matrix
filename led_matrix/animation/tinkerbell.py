#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import colorsys
from led_matrix.animation.animation import Animation


def hsv2rgb(h,s,v):
    r,g,b = colorsys.hsv_to_rgb(h/360,s/100,v/100)
    return int(round(r*255)),int(round(g*255)),int(round(b*255))

def hsv2rgb_value(h,s,v):
    r,g,b = hsv2rgb(h,s,v)
    return r<<16 | g<<8 | b

def rgb2hsv(r,g,b):
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    return int(round(h*360)),int(round(s*100)),int(round(v*100))

def rgb_value2hsv(color):
    r,g,b = (color&0xFF0000)>>16, (color&0xFF00)>>8 , color&0xFF
    return rgb2hsv(r,g,b)


def brightness(color,percentage=100):
    r,g,b = (color >> 16), (color >> 8) & 0xFF, color & 0xFF
    nr = int(r*percentage/100)
    ng = int(g*percentage/100)
    nb = int(b*percentage/100)
    return (nr<<16) | (ng<<8) | nb


def brightness_diff(color1,color2):
    color1 &= 0xFF00
    color2 &= 0xFF00
    return int(color2*100/color1)


class Particle(object):
    def __init__(self,x,y,screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.effects = []

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def add_effect(self,effect):
        self.effects.append(effect)

    def run(self):
        for effect in self.effects:
            effect.apply(self)
            if effect.is_finished():
                self.effects.remove(effect)

    def getbr(self):
        return rgb_value2hsv(self.get())[2]

    def get(self):
        return self.screen[(self.x,self.y)]

    def set(self,val):
        self.screen[(self.x,self.y)] = val

    def setbr(self,br):
        h,s,v = rgb_value2hsv(self.get())
        v = br
        self.set(hsv2rgb_value(h,s,v))

    def __repr__(self):
        return "(%r,%r):%s" % (self.x,self.y,self.effects)

    def is_died(self):
        return len(self.effects) == 0


class Effect(object):
    def __init__(self,every=None):
        self.every = every
        self.last_apply = 0
        self.finished = False

    def need_apply(self):
        return not self.every or time.time()*1000 - self.last_apply > self.every

    def apply(self,particle):
        if self.need_apply():
            self.run(particle)
            self.last_apply = time.time()*1000

    def run(self,particle):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__

    def is_finished(self):
        return self.finished


class StepEffect(Effect):
    def __init__(self,step=10,*args,**kargs):
        super().__init__(*args,**kargs)
        self.step = step


class DimOff(StepEffect):
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)

    def run(self,particle):
        br = max(0,particle.getbr()-self.step)
        particle.setbr(br)
        self.finished = (br == 0)


class DimOn(StepEffect):
    def __init__(self,brightness,*args,**kargs):
        super().__init__(*args,**kargs)
        self.brightness = brightness 

    def run(self,particle):
        br = min(self.brightness,particle.getbr()+self.step)
        particle.setbr(br)
        self.finished = (br == self.brightness)


class Glow(StepEffect):
    def __init__(self,max_glow=50,min_glow=10,*args,**kargs):
        super().__init__(*args,**kargs)
        self.direction = 1
        self.maxbr = max_glow
        self.minbr = min_glow

    def run(self,particle):
        br = particle.getbr()
        if br <= self.minbr:
            self.direction = 1
        elif br >= self.maxbr:
            self.direction = -1
        particle.setbr(br+(self.direction*self.step))


class TinkerBell(Animation):
    class Firefly(object):
        def __init__(self,x,y,screen,color=275):
            self.x = x
            self.y = y
            self.particles = []
            self.screen = screen
            self.hue = color
            self.last_moved = 0
            self.next_x = 0
            self.next_y = 0
            self.last_move = time.time()
            self.update_step = 150

        def init(self):
            self.display()

        def choose_destination(self):
            self.next_x = random.randint(0,7)
            self.next_y = random.randint(0,7)

        def set_brightness(self,brightness=100,x=None,y=None):
            x = self.x if x is None else x
            y = self.y if y is None else y
            self.screen[(x,y)] = hsv2rgb_value(self.hue,100,brightness)

        def get_glow_coordinates(self):
            for i in (0,):
                for j in (0,):
                    if self.in_screen(self.x+i,self.y+j):
                        if (i,j) != (0,0) and (abs(i),abs(j)) != (1,1):
                            yield (self.x+i,self.y+j)

        def add_glow(self):
            for i,j in self.get_glow_coordinates():
                self.set_brightness(2,i,j)
                self.add_particle(Particle(i,j,self.screen),Glow(every=self.update_step,min_glow=5,max_glow=36,step=4))

        def display(self):
            self.set_brightness(5)
            self.add_particle(Particle(self.x,self.y,self.screen),Glow(max_glow=90,min_glow=15,every=self.update_step,step=10))
            self.add_glow()

        def is_near(self,x,y):
            return abs(self.x-x) <= 1 and abs(self.y-y) <= 1

        def in_screen(self,x,y):
            return x < self.screen.width and x >= 0 and y < self.screen.height and y >=0 

        def add_trace(self,x,y,brightness):
            if self.in_screen(x,y):
                self.set_brightness(brightness,x,y)
                self.add_particle(Particle(x,y,self.screen),DimOff(every=self.update_step))

        def add_particle(self,particle,effect):
            if particle in self.particles:
                self.particles.remove(particle)
            self.particles.append(particle)
            particle.add_effect(effect)

        def move(self):
            if self.x == self.next_x and self.y == self.next_y:
                self.choose_destination()

            if self.x > self.next_x: dx = -1
            elif self.x < self.next_x: dx = 1
            else: dx = 0

            if self.y > self.next_y: dy = -1
            elif self.y < self.next_y: dy = 1
            else: dy = 0

            if not self.in_screen(self.x+dx,self.y): dx=0
            if not self.in_screen(self.x,self.y+dy): dy=0

            br = 60
            if dx != 0 or dy != 0:
                particle = Particle(self.x,self.y,self.screen)
                self.add_particle(particle,DimOff(every=250,step=5))
                for i,j in self.get_glow_coordinates():
                    particle = Particle(i,j,self.screen)
                    self.add_particle(particle,DimOff(every=250,step=5))
#            if dx > 0:
#                self.add_trace(self.x,self.y+1,br)
#                self.add_trace(self.x,self.y-1,br)
#            if dy != 0:
#                self.add_trace(self.x+1,self.y,br)
#                self.add_trace(self.x-1,self.y,br)

            self.x += dx
            self.y += dy

            self.display()
            self.last_move = time.time()*100

        def update_particles(self):
            for particle in self.particles:
                particle.run()

        def update(self):
            if random.randint(0,1000) > 900 and time.time()*100-self.last_move > 50:
                self.move()
                pass
            self.update_particles()

    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        self.nb = 1

    def run(self):
        #fireflies = [TinkerBell.Firefly(0,0,self.screen),TinkerBell.Firefly(6,6,self.screen)]
        fireflies = [TinkerBell.Firefly(7,7,self.screen,color=275)]
        for firefly in fireflies:
            firefly.init()
        while not self.stop_received:
            for firefly in fireflies:
                firefly.update()
            self.screen.render()
            time.sleep(0.01)
