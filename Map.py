import pygame
from Player import Player

class Map(object):

	def __init__(self):
		self.players = { }

	def addPlayer(self, name):
		# TODO: check for duplicates
		self.players[name] = Player(name)

	def drawSurface(self):
		surface = pygame.Surface((1024, 768))

		for key in self.players:
			pygame.draw.rect(surface, (255,255,255),
				(self.players[key].x, self.players[key].y, 25,25))

		return surface
