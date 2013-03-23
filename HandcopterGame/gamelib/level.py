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

import pygame
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from fairy import Fairy
from ghost import Ghost
from wall import Wall

import sys

class Levels:

    def __init__(self):
        self.levels = []
        self.level = None
        self.restore_all_levels()
        
    def get_next_level(self):
        lvl = self.levels.pop(0)
        self.level = lvl()
        return self.level

    def reload_level(self):
        self.level = type(self.level)()
        return self.level

    def restore_all_levels(self):
        self.levels = [Level1]
        
class BaseLevel(object):
    
    def __init__(self, height, levelname, width = 600):
        self.height = height
        self.width = width
        self.name = levelname
        self.walls = Group()
        self.boundaries = Group()
        self.create_walls()
        self.fairies = Group()
        self.ghosts = Group()
        self.fiends = Group()
        self.game_elements = Group()
        
    def create_walls(self):
        #startPlatform = Wall(0, 110, 130, 60)
        wallTop = Wall(0, 0, self.width, int(150 * 0.75))
        wallBottom = Wall(0, self.height - int(150 * 0.75), self.width, int(150 * 0.75))
        #wallLeft = Wall(0, 0, 32, self.height)
        #wallRight = Wall(self.width - 32, 0, 32, self.height)
        self.walls.add((wallTop, wallBottom))
        self.boundaries.add((wallTop, wallBottom))


    def pack(self):
        self.game_elements.add(self.fairies)
        self.game_elements.add(self.ghosts)
        self.game_elements.add(self.walls)
        self.game_elements.add(self.fiends)

class Level1(BaseLevel):
    def __init__(self):
        BaseLevel.__init__(self, 600, '1', width=800)

    
