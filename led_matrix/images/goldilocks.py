#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from led_matrix.animation.sprite import Sprite
from led_matrix.images.image import StaticImage

class Bear1(StaticImage):
    DEFAULT_COLOR = 0xFF
    DEFAULT_PATTERN = {"+":1,"#":0x8c2300,"@":0,"*":0xe0902d}
    IMAGE = \
""".#.##.#.
..####..
..#@#@..
.###@#..
##***##.
*#***#*.
.+++++..
.#*.*#..
"""

class Bear2(Bear1):
    IMAGE = \
""".#.##.#.
..####..
..#@#@..
.###@#..
##***##.
*#***#*.
.+++++..
..#*.*#.
"""


class BabyBear1(Bear1):
    IMAGE = \
"""........
........
.#.##.#.
..#@#@..
.###@#..
##***##.
*#+++#*.
..*.*...
"""


class BabyBear2(Bear1):
    IMAGE = \
"""........
........
.#.##.#.
..#@#@..
.###@#..
##***##.
*#+++#*.
.*...*..
"""


class Bear(Sprite):
    def __init__(self,color=0xFF):
        images = [Bear1(color=color),Bear2(color=color)]
        super().__init__(images=images)


class BabyBear(Sprite):
    def __init__(self,color=0xFF):
        images = [BabyBear1(color=color),BabyBear2(color=color)]
        super().__init__(images=images)
