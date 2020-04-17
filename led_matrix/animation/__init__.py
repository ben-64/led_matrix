#!/usr/bin/env python3

from led_matrix.tools.importer import add_classes_to_globals
from led_matrix.animation.animation import Application

load_classes = add_classes_to_globals(__file__,__name__,lambda c:issubclass(c,Application))
