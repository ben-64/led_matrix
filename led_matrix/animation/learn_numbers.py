#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
from led_matrix.fonts.font4x5 import Font4x5
from led_matrix.fonts.adafruit import *
from led_matrix.animation.animation import TextApplication

class LearnNumbers(TextApplication):

    def __init__(self,numbers=[11,12,13,14],*args,**kargs):
        super().__init__(*args,**kargs)
        self.numbers = numbers

    def update(self):
        self.print_text("%u" % random.choice(self.numbers),font=AdaFruit(),space=2)


class Addition(TextApplication):

    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        self.refresh = 1


    def update(self):
        x = random.randint(0,20)
        y = random.randint(0,20)
        self.print_text("%u+%u" % (x,y),font=Font4x5(),space=1)
        time.sleep(8)
        self.print_text("%u" % (x+y),font=Font4x5(),space=1)
        time.sleep(2)

