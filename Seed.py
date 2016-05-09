import pygame

from random import *

class Seed(pygame.Rect):
	def __init__(self, bounds):
		pygame.Rect.__init__(self,0,0,25,25)

		self.bounds = bounds
		self.move()

	def move(self):
		x = randint(0, self.bounds.w - 25);
		self.x = x - (x % 25)
		y = randint(0, self.bounds.h - 25);
		self.y = y - (y % 25)

	def drawToSurface(self, surface):
		pygame.draw.rect(surface, (255,255,255), self)
