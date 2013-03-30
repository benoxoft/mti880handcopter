#! /usr/bin/env python

#    Copyright (C) 2010  Benoit <benoxoft> Paquet
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pygame.sprite import Sprite
from pygame.rect import Rect

from movement import Movement

import pygame

import media
import random

class Ghost(Sprite):

    def __init__(self, posx, posy):
        Sprite.__init__(self)
        self.move = Movement(self, thrust_strength = 1000,
                             accelx = 1000,
                             accely = 1000,
                             maxspeedx = 153,
                             maxspeedy = 153,
                             gravity = 0,
                             posx = posx,
                             posy = posy)

        if random.randint(0, 2) == 1:        
            self.image = media.load_image('Cone.png')
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (int(self.rect.width*1.5), int(self.rect.height*1.5)))
        else:
            self.image = media.load_image('Trou.png')
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (self.rect.width*2, self.rect.height*2))
            
        self.rect = self.image.get_rect()
    def update(self, tick):
        self.move.moveleft(tick)
        self.move.calculate_movement(tick)
        self.rect.x = self.move.posx
        self.rect.y = self.move.posy        
