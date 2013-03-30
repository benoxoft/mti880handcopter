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

from gamelib.MainChar import MainChar
from gamelib.wall import Wall
from gamelib.camera import Camera
from gamelib.fairy import Fairy
from gamelib.level import *
from gamelib.ui import *
from gamelib.brain import *
from gamelib import media

import socket
import threading

class GameControl:

    def __init__(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.downKeyDown = False
        self.keepPlaying = True
        self.ghost_add = 0
        
    def reset(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.downKeyDown = False
        self.keepPlaying = True
        
def show_message(msg):
    draw(0)
    font = media.get_font(44)
    s = font.render(msg, True, (255,255,255))
    screen.blit(s, (300 - s.get_width() / 2, 200))
    pygame.display.update()
    pygame.time.delay(1500)
    clock.tick()

def show_intro():
    draw(1)
    w = Surface((640, 460))
    w.fill(pygame.color.Color('black'))
    font = media.get_font(16)
    
    l1 = font.render('MTI880 Handcopter', True, (255,255,255))
    l2 = font.render('Open your hand to move up', True, (255,255,255))
    l3 = font.render('Close your hand to move down', True, (255,255,255))
    l4 = font.render('Avoid obstacles!' , True, (255,255,255))
    l5 = font.render('Avoid ghosts!', True, (255,255,255))

    lspace = font.render('Press <spacebar> to play', True, (255,255,255))
    lesc = font.render('Press <Esc> to quit', True, (255,255,255))
    lname = media.get_font(10).render('Everything by Benoit <benoxoft> Paquet', True, (255,255,255))

    x = 80
    w.blit(l1, (x, 180))
    w.blit(l2, (x, 210))
    w.blit(l3, (x, 240))
    w.blit(l4, (x, 290))
    #w.blit(l5, (x, 320))
    
    w.blit(lspace, (30, 380))
    w.blit(lesc, (420, 380))
    #w.blit(lname, (320 - lname.get_width() / 2, 440))
    
    screen.blit(w, (80, 80))    
    pygame.display.update()

    waiting = True    
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    waiting = False
                elif e.key == pygame.K_ESCAPE:
                    import sys
                    sys.exit(0)
        
    pygame.time.delay(100)
    clock.tick()
    
def ghost_kill():
    show_message('Oww...')
    mainchar.remove_life()
    kill_level(levels.level)
    load_level(levels.reload_level())
    
def no_more_life():
    show_message('Game Over!')
    pygame.time.delay(1500)
    
    kill_level(levels.level)
    levels.restore_all_levels()
    load_level(levels.get_next_level())
    mainchar.lives = 3
    show_intro()
    
def load_level(level):
    cam.level = level
    mainchar.move.add(level.walls)
    mainchar.fairies_to_catch.add(level.fairies)
    mainchar.set_init_pos()
    mainchar.fuel = 10000
    cam.set_init_pos()
    for fairy in level.fairies:
        fairy.brain = FairyBrain(fairy, mainchar)
        fairy.move.add(level.walls)

    for ghost in level.ghosts:
        ghost.brain = GhostBrain(ghost, mainchar)
        ghost.brain.kill_event = ghost_kill
        ghost.move.add(level.boundaries)

    level.pack()

def kill_level(level):
    mainchar.move.empty()
    mainchar.fairies_to_catch.empty()
    mainchar.caught_fairies.empty()
    pygame.event.get()
    g.reset()
    
def draw(tick):
    level = levels.level
    
    if tick > 0:
        mainchar.update(tick)
        cam.update()
        ui.update(tick)    
    screen.blit(ui.bg, ui.bg.get_rect())
    draw_elements(level.ghosts, tick)
    screen.blit(mainchar.image,
                    pygame.rect.Rect(mainchar.rect.x - cam.x,
                             mainchar.rect.y - cam.y,
                             mainchar.rect.w - cam.w,
                             mainchar.rect.h - cam.h))


        
    pygame.display.update()
    pygame.time.delay(16)

def draw_elements(elements, tick):
    for element in elements:
        if tick > 0:
            element.update(tick)            
        screen.blit(element.image,
                        pygame.rect.Rect(element.rect.x - cam.x,
                                       element.rect.y - cam.y,
                                       element.rect.w - cam.w,
                                       element.rect.h - cam.h))


def manage_ghost(tick):
    g.ghost_add += tick
    if g.ghost_add > 2000:
        print g.ghost_add
        ghost = Ghost(900, random.random() * 400 + 100)
        ghost.brain = GhostBrain(ghost, mainchar)
        ghost.brain.kill_event = ghost_kill
        ghost.move.add(levels.level.boundaries)        
        levels.level.ghosts.add(ghost)
        g.ghost_add = 0

    for ghost in levels.level.ghosts:
        #if pygame.sprite.collide_mask(mainchar, ghost) is not None:
        #    ghost_kill()
        #distance = math.sqrt(
        #    abs(ghost.rect.centerx - mainchar.rect.centerx)**2 +
        #    abs(ghost.rect.centery - mainchar.rect.centery)**2)
        #if distance <= 22:
        #    pass#ghost_kill()            
        mr = pygame.Rect((mainchar.rect.left + 18, mainchar.rect.top + 14), (mainchar.rect.width - 36, mainchar.rect.height - 28))
        gr = pygame.Rect((ghost.rect.left + 3, ghost.rect.top + 3), (ghost.rect.width - 6, ghost.rect.height - 6))

        if mr.colliderect(gr):
            ghost_kill()
        if ghost.move.posx < -60:
            levels.level.ghosts.remove(ghost)
            
def main():
    
    while g.keepPlaying:
        listen()
        tick = clock.tick()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    g.leftKeyDown = True
                elif e.key == pygame.K_RIGHT:
                    g.rightKeyDown = True
                elif e.key == pygame.K_UP:
                    g.upKeyDown = True
                elif e.key == pygame.K_DOWN:
                    g.downKeyDown = True
                elif e.key == pygame.K_SPACE:
                    g.upKeyDown = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    g.leftKeyDown = False
                elif e.key == pygame.K_RIGHT:
                    g.rightKeyDown = False
                elif e.key == pygame.K_UP:
                    g.upKeyDown = False
                elif e.key == pygame.K_DOWN:
                    g.downKeyDown = False
                elif e.key == pygame.K_SPACE:
                    g.upKeyDown = False
                elif e.key == pygame.K_ESCAPE:
                  g.keepPlaying = False  

        if g.leftKeyDown:
            mainchar.move.speedy = 0
        #if g.rightKeyDown:
        #    mainchar.moveright(tick)
        if g.upKeyDown:
            mainchar.moveup(tick)
        if g.downKeyDown:
            mainchar.movedown(tick)
        draw(tick)
        manage_ghost(tick)

def listen():
    try:
        s = sock.recv(1024)
    except Exception,e:
        print e
        return
    cmds = s.split("\n")
    try:
        #print s
        cmd = float(cmds[-2])
        g.reset()
        if cmd < 0:
            g.downKeyDown = True
        elif cmd == 0:
            g.leftKeyDown = True
        else:
            g.upKeyDown = True
    except Exception,e:
        print e
        
if __name__ == '__main__':   
    
    sock = socket.socket()
    try:
        sock.connect(('localhost', 5030))
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    except Exception, e:
        print e
    print "Connected!"

    pygame.init()

    #game objects
    #screen = pygame.display.set_mode((800, 600))
    screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE)

    pygame.display.set_caption('MTI880 Handcopter!')
    pygame.mouse.set_visible(False)
    
    g = GameControl()
    
    #main character
    mainchar = MainChar()
    mainchar.no_more_life_event = no_more_life

    font = media.get_font(20)

    ui = GameUI(mainchar)
    cam = Camera(mainchar)

    levels = Levels()
    load_level(levels.get_next_level())

    clock = pygame.time.Clock()

    show_intro()

    main()
