#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from led_matrix.animation.sprite import ColorSprite
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


class Pacman(ColorSprite):
    def __init__(self,color=0xFFFF00):
        images = [ImageStr(_PACMAN_CLOSE),ImageStr(_PACMAN_OPEN)]
        super().__init__(images=images,color=color)

_GHOST = \
""".......
.#####.
#######
#.*#.*#
#######
#######
#######
#.#.#.#"""


class Ghost(ColorSprite):
    def __init__(self,color=0xFF):
        images = [ImageStr(_GHOST,{"#":1,"*":0xFFFFFF})]
        super().__init__(images=images,color=color)
