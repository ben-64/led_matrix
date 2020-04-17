#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
from led_matrix.animation.animation import Animation
from led_matrix.image import Image

class Sprite(object):
    """ Set of images """
    def __init__(self,images=None):
        self.images = images if images else self.IMAGES
        self.width = images[0].width
        self.height = images[0].height
        self.current_image = 0

    def next(self):
        self.current_image = (self.current_image + 1) % len(self.images)

    def set_image(self,i):
        self.current_image = i%len(self.images)

    def get(self):
        return self.images[self.current_image]

    def __getitem__(self,i):
        return self.images[self.current_image][i]

    def __len__(self):
        return len(self.images)

    def print_current_image(self):
        self.get().display()


class MultipleSprite(Sprite):
    """ Set of sprite, to concatenate animations """
    def __init__(self,sprites,space=1):
        big_sprite = []
        greatest_number_of_sprites = max(map(len,sprites))
        for num_image in range(greatest_number_of_sprites):
            sprites[0].set_image(num_image)
            img = sprites[0].get()
            for sprite in sprites[1:]:
                sprite.set_image(num_image)
                img = img.concatenate(sprite.get(),space=space)
            big_sprite.append(img)
        super().__init__(big_sprite)


class SpriteAnimation(Animation):
    """ Animation class to alternate between images of a Sprite """
    def __init__(self,sprite,*args,**kargs):
        super().__init__(refresh=0.1,*args,**kargs)
        self.sprite = sprite
 
    def run(self):
        # Part of sprite
        for nb_col in range(1,self.sprite.width+1):
            column_start = self.sprite.width - nb_col
            for i in range(nb_col):
                for j in range(self.sprite.height):
                    self.screen[(i,j)] = self.sprite[column_start,j]
                column_start += 1
            self.sprite.next()
            self.screen.render()
            time.sleep(self.refresh)

        for start_col in range(1,self.screen.width):
            # Clean last column
            for j in range(self.screen.height):
                self.screen[(start_col-1,j)] = 0
            
            self.screen.image(self.sprite.get(),start_col,0)
            self.sprite.next()
            self.screen.render()
            time.sleep(self.refresh)

        for j in range(self.screen.height):
            self.screen[(31,j)] = 0

        self.screen.render()
