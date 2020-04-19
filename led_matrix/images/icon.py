#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from led_matrix.images.image import StaticImage

class ARROW_UP(StaticImage):
    DEFAULT_COLOR = 0xFF00
    IMAGE = \
""".....###
......##
.....#.#
....#...
...#....
..#.....
.#......
#......."""


class ARROW_DOWN(StaticImage):
    DEFAULT_COLOR = 0xFF0000
    IMAGE = \
"""#.......
.#......
..#.....
...#....
....#...
.....#.#
......##
.....###"""


class SMILEY(StaticImage):
    DEFAULT_COLOR = 0xFFFF00
    IMAGE = \
"""........
..####..
.#.##.#.
########
########
#.####.#
.#....#.
..####.."""


class DRAGON(StaticImage):
    DEFAULT_PATTERN = {"#":1,"*":0xFF0000,"@":0xFFFFFF}
    DEFAULT_COLOR = 0xFF00
    IMAGE = \
"""..*###..
.*#.####
..@@####
.*@@####
..*@@@@.
#*##@@#.
.###@@##
..**.**."""
