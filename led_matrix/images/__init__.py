#!/usr/bin/env python3

from led_matrix.tools.importer import add_classes_to_globals
from led_matrix.animation.sprite import Sprite
from led_matrix.images.image import Image
from led_matrix.images.gridimage import GridImage

load_classes = add_classes_to_globals(__file__,__name__,lambda c:issubclass(c,Image) or issubclass(c,GridImage) or issubclass(c,Sprite))
