#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Credit: https://github.com/gineer01/matrix-rain/blob/master/matrix.py

import random
import time
from led_matrix.animation.animation import Animation

#How fast the rain should fall. In config, we change it according to screen.
FALLING_SPEED = 2

#The max number of falling rains. In config, we change it according to screen.
MAX_RAIN_COUNT = 15

COLORS = [0x4400,0x8800,0xBB00,0xFF00]

class Matrix(Animation):
    def __init__(self,speed=0.1,*args,**kargs):
        super().__init__(*args,**kargs)
        self.speed = speed
        self.max_rain_count = self.screen.width//3
        self.falling_speed = 1 + self.screen.height//25
        self.pool = list(range(self.screen.width))
        self.rains = []

    def random_rain_length(self):
        return random.randint(self.screen.height//2, self.screen.height)

    def show_rain(self, head, middle, tail, x, speed):
        for i in range(max(0,tail-speed),tail):
            self.screen[(x,i)] = 0
        for i in range(tail, min(head,self.screen.height)):
            self.screen[(x,i)] = COLORS[(i-tail)%len(COLORS)]

    def rain(self):
        while True:
            x = random.choice(self.pool)
            self.pool.remove(x)
            max_length = self.random_rain_length()
            speed = random.randint(1, FALLING_SPEED)
            yield from self.animate_rain(x, max_length, speed)
            self.pool.append(x)

    def animate_rain(self, x, max_length, speed=FALLING_SPEED):
        head, middle, tail = 0,0,0

        while tail < self.screen.height:
            middle = head - max_length//2
            if (middle < 0):
                middle = 0

            tail = head - max_length
            if (tail < 0):
                tail = 0

            self.show_rain(head, middle, tail, x, speed)

            head = head + speed
            yield

    def add_rain(self):
        if (len(self.rains) < MAX_RAIN_COUNT) and (len(self.pool) > 0):
            self.rains.append(self.rain())

    def run(self):
        while not self.stop_received:
            self.add_rain()
            for r in self.rains:
                next(r)
            self.screen.render()
            time.sleep(self.speed)
