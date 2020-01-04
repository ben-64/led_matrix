#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from led_matrix.animation.animation import Animation

PACMAN1 = [ 0,0,0,0,0,0,0,0,
            0,0,1,1,1,1,0,0,
            0,1,1,1,0,1,1,0,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
            0,1,1,1,1,1,1,0,
            0,0,1,1,1,1,0,0
        ]

PACMAN2 = [ 0,0,0,0,0,0,0,0,
            0,0,1,1,1,1,0,0,
            0,1,1,1,0,1,1,0,
            1,1,1,1,1,1,0,0,
            1,1,1,1,1,0,0,0,
            1,1,1,1,1,1,0,0,
            0,1,1,1,1,1,1,0,
            0,0,1,1,1,1,0,0
        ]


class Pacman(Animation):
    def __init__(self,color=0xffe900,*args,**kargs):
        super().__init__(refresh=0.1,*args,**kargs)
        self.pacman_open = list(map(lambda x:0 if x==0 else color,PACMAN2))
        self.pacman_closed = list(map(lambda x:0 if x==0 else color,PACMAN1))
 
    def run(self):
        width_pacman = 8
        start_x = 0
        
        x = 1
        is_pacman_open = True

        # Part of Pacman
        for nb_col in range(1,width_pacman+1):
            column_start = width_pacman - nb_col
            for i in range(nb_col):
                for j in range(8):
                    self.screen[(i,j)] = self.pacman_open[j*8+column_start] if is_pacman_open else self.pacman_closed[j*8+column_start]
                column_start += 1
            is_pacman_open = not is_pacman_open
            self.screen.render()
            time.sleep(self.refresh)

        for start_col in range(1,self.screen.width):
            # Clean last column
            for j in range(self.screen.height):
                self.screen[(start_col-1,j)] = 0
            
            if is_pacman_open:
                self.screen.image(self.pacman_open,start_col,0)
            else:
                self.screen.image(self.pacman_closed,start_col,0)
            is_pacman_open = not is_pacman_open
            self.screen.render()
            time.sleep(self.refresh)

        for j in range(self.screen.height):
            self.screen[(31,j)] = 0

        self.screen.render()
