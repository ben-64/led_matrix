#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import json
import socket
from threading import Thread

from led_matrix.animation.quizz import Challenge

def generate_number(num,sz=3):
    s = ""
    for i in range(sz):
        if i == 0:
            x = random.choice(num)
            while x == "0":
                x = random.choice(num)
        else:
            x = random.choice(num)
        s += x
    return int(s)

def generate_mod2(sz=3):
    return generate_number("02468",sz)

def generate_easy_double(sz=3):
    return generate_number("01234",sz)

class Split2(Challenge):
    def get_problem(self):
        x = generate_easy_double()
        return str(2*x),str(x).encode("ascii")

class Double(Challenge):
    def get_problem(self):
        x = generate_easy_double()
        return str(x),str(2*x).encode("ascii")

class Complement(Challenge):
    def __init__(self,a=10,*args,**kargs):
        super().__init__(*args,**kargs)
        self.a = a

    def get_problem(self):
        x = random.randint(0,10)
        return str(x),str(self.a-x).encode("ascii")


