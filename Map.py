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
			# make position updates to collition rectangles from velocity
			self.players[key].update()

			# draw all the rectangles
			#surface.blit(self.players[key].drawSurface(), (0,0))
			self.players[key].drawToSurface(surface)

		return surface
