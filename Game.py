#!/usr/bin/python

import pygame
import math
import sys
from Map import Map
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255, 255, 255)

class Game(object):
	def __init__(self):
		#self.screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode((1024, 768))
		self.clock = pygame.time.Clock()
		self.map = Map()
		self.player = Map().getPlayer()

		pygame.mouse.set_visible(False)
		self.run()

	def run(self):
		while 1:
			self.clock.tick(30)

			hor = 0
			vert = 0

			for event in pygame.event.get():
				if not hasattr(event, 'key'): continue
				if not event.type == KEYDOWN: continue
				if event.key == K_ESCAPE: sys.exit(0)
				if event.key == K_LEFT: hor = -25
				if event.key == K_RIGHT: hor = 25
				if event.key == K_UP: vert = -25
				if event.key == K_DOWN: vert = 25
				if event.key == K_SPACE: self.player = self.map.getPlayer()

			self.map.players[self.player].x += hor
			self.map.players[self.player].y += vert

			self.screen.blit(self.map.drawSurface(), (0,0))
			pygame.display.flip()
 
if __name__ == "__main__":
	game = Game()
