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

#Main Character of the game.

from pygame.sprite import Sprite, Group
from movement import Movement

import pygame
import math
import media

class MainChar(Sprite):

    def __init__(self):
        self.move = Movement(self, thrust_strength = 100000,
                             accelx = 100000,
                             accely = 100000,
                             maxspeedx = 120,
                             maxspeedy = 120,
                             gravity = 0,
                             posx=200,
                             posy=200)
        self.hunter = media.load_image('hunter.png').convert_alpha()
        self.firstupdate = False
        self.image = self.hunter
        self.rect = self.image.get_rect()
        self.imgflip = False
        self.dir = 1

        self.fuel = 10000
        self.lives = 3
        
        self.caught_fairies = Group()
        self.fairies_to_catch = Group()

        self.out_of_fuel_event = None
        self.no_more_life_event = None
        self.all_fairies_caught_event = None
        self.moveright(1000)
        
    def set_init_pos(self):
        self.move.posx = 200
        self.move.posy = 200
        self.move.speedx = 0
        self.move.speedy = 0
        self.dir = 1
        self.flip()
        
    def flip(self):
        if not self.imgflip and self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = True
        elif self.imgflip and self.dir == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = False
                
    def moveright(self, tick):
        self.dir = 1
        self.flip()
        self.move.moveright(tick)
        
    def moveup(self, tick):
        self.move.thrust(tick)
    
    def movedown(self, tick):
        self.move.movedown(tick)
            
    def update(self, tick):
        if not self.firstupdate:
            self.image = self.hunter
            self.imgflip = False
            self.flip()
        self.firstupdate = False
        
        self.move.calculate_movement(tick)
            
        self.rect.x = self.move.posx
        self.rect.y = self.move.posy
        
    def raise_no_more_life_event(self):
        self.no_more_life_event()

    def remove_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.raise_no_more_life_event()
                    
