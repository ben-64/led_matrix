#!/usr/bin/env python3

import sys


def add_parameters(constructor,parameter):
    """ Ugly : Add parameters to an existing constructor """
    parenthesis = constructor.rfind(')')
    if parenthesis == -1:
        return None
    sep = "," if constructor[parenthesis-1] != '(' else ""
    return constructor[:parenthesis] + sep + ",".join(parameter) + constructor[parenthesis:]


def get_screen(screen):
    """ Return screen corresponding to string """
    import led_matrix.screens
    led_matrix.screens.load_classes(globals())
    try:
        return eval(screen)
    except:
        screens = get_all_subclasses(Screen)
        print("Unable to find screen %s : Possible values: %s" % (screen,",".join([x.__name__ for x in screens])))
        sys.exit(1)


def get_animation(animation,screen):
    """ Return animation corresponding to string """
    import led_matrix.animation
    from led_matrix.animation.sprite import MultipleSprite
    from led_matrix.animation.images.pacman import Pacman,Ghost
    led_matrix.animation.load_classes(globals())
    constructor = add_parameters(animation,["screen=screen"])
    try:
        return eval(constructor)
    except:
        apps = get_all_subclasses(Application)
        print("Unable to find application %s : Possible values: %s" % (animation,",".join([x.__name__ for x in apps])))
        sys.exit(1)


def get_all_subclasses(cls):
    """ Return all subclasses of cls """
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses
