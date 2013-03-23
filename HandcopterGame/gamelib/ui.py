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

from pygame.surface import Surface
import pygame
import math
import media

class GameUI:
    def __init__(self, mainchar):
        self.bg = Surface((800, 600))
        self.mainchar = mainchar
        self.layer = self.create_layer()
        self.top = self.create_top()
        self.bottom = self.create_bottom()
        self.scroll = 0
        self.scroll_top = 0
        
    def create_layer(self):
        bgimg = media.load_image('bg.png').convert()
        rbgimg = bgimg.get_rect()
        rows = int(600 / rbgimg.height) + 2
        
        layer = Surface((rbgimg.width, 600))
        for y in xrange(rows):
            layer.blit(bgimg, rbgimg)
            rbgimg = rbgimg.move([0, rbgimg.height])
        return layer
    
    def create_top(self):
        bgimg = media.load_image('tile_wall.png').convert()
        rbgimg = bgimg.get_rect()
        self.top_size = rbgimg.width
        cols = int(1000 / rbgimg.width)
        
        top = Surface((1000, rbgimg.height))
        for x in xrange(cols):
            top.blit(bgimg, rbgimg)
            rbgimg = rbgimg.move([rbgimg.width, 0])
        return top
    
    def create_bottom(self):
        bgimg = media.load_image('tile_wall.png').convert()
        bgimg = pygame.transform.flip(bgimg, False, True)
        rbgimg = bgimg.get_rect()
        cols = int(1000 / rbgimg.width)
        
        top = Surface((1000, rbgimg.height))
        for x in xrange(cols):
            top.blit(bgimg, rbgimg)
            rbgimg = rbgimg.move([rbgimg.width, 0])
        return top
    
    def update(self, tick):
        self.scroll += tick / 6
        self.scroll_top += tick / 6
        
        rlayer = self.layer.get_rect()
        rlayer = rlayer.move((-self.scroll, -18))
        columns = int(800 / rlayer.width) + 2
        for x in xrange(columns):
            self.bg.blit(self.layer, rlayer)
            rlayer = rlayer.move((rlayer.width, 0))
        if self.scroll > rlayer.width:
            self.scroll -= rlayer.width
        
        rtop = self.top.get_rect()
        rbottom = self.bottom.get_rect()
        
        rtop = rtop.move((-self.scroll_top, 6))
        rbottom = rbottom.move((-self.scroll_top, self.bg.get_rect().height - rbottom.height - 6))
        self.bg.blit(self.top, rtop)
        self.bg.blit(self.bottom, rbottom)
            
        if self.scroll_top > self.top_size:
            self.scroll_top -= self.top_size