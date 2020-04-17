#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from led_matrix.animation.sprite import Sprite
from led_matrix.image import StaticImage

class PACMAN_CLOSE(StaticImage):
    IMAGE = \
"""........
..####..
.###.##.
########
########
########
.######.
..####.."""


class PACMAN_OPEN(StaticImage):
    IMAGE = \
"""........
..####..
.###.##.
######..
#####...
######..
.######.
..####.."""


class Pacman(Sprite):
    def __init__(self,color=0xFFFF00):
        images = [PACMAN_CLOSE(color=color),PACMAN_OPEN(color=color)]
        super().__init__(images=images)

class GHOST(StaticImage): 
    IMAGE = \
""".......
.#####.
#######
#.*#.*#
#######
#######
#######
#.#.#.#"""


class Ghost(Sprite):
    def __init__(self,color=0xFF):
        images = [GHOST({"#":1,"*":0xFFFFFF},color)]
        super().__init__(images=images)
