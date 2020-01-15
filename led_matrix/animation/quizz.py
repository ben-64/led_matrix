#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import json
from led_matrix.fonts.font4x5 import Font4x5
from led_matrix.fonts.adafruit import *
from led_matrix.animation.animation import TextApplication,ScrollText

class Quizz(ScrollText):

    def __init__(self,conf,*args,**kargs):
        super().__init__(*args,**kargs)
        self.load_conf(conf)

    def load_conf(self,conf):
        with open(conf,"r") as f:
            self.quizz = json.load(f)

    def set_text(self):
        problem = random.choice(self.quizz)
        question = eval(problem["question"])
        return question
