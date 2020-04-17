#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from led_matrix.animation.sprite import Sprite
from led_matrix.image import ImageStr

_PACMAN_CLOSE = \
"""........
..####..
.###.##.
########
########
########
.######.
..####.."""

_PACMAN_OPEN = \
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
        images = [ImageStr(_PACMAN_CLOSE,color=color),ImageStr(_PACMAN_OPEN,color=color)]
        super().__init__(images=images)

_GHOST = \
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
        images = [ImageStr(_GHOST,{"#":1,"*":0xFFFFFF},color)]
        super().__init__(images=images)
