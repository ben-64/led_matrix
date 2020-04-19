#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from led_matrix.animation.sprite import Sprite
from led_matrix.images.image import StaticImage

class PACMAN_CLOSE(StaticImage):
    DEFAULT_COLOR = 0xFFFF00
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
    DEFAULT_COLOR = 0xFFFF00
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
    DEFAULT_COLOR = 0xFF
    IMAGE = \
""".......
.#####.
#######
#.*#.*#
#######
#######
#######
#.#.#.#"""

class GHOST2(StaticImage): 
    DEFAULT_COLOR = 0xFF
    IMAGE = \
""".......
.#####.
#######
#*.#*.#
#######
#######
#######
.#.#.#."""


class Ghost(Sprite):
    def __init__(self,color=0xFF):
        images = [GHOST({"#":1,"*":0xFFFFFF},color),GHOST2({"#":1,"*":0xFFFFFF},color)]
        super().__init__(images=images)
