import pygame
from Player import Player

class Map(object):

	def __init__(self, bounds):
		self.players = { }

		self.bounds = bounds

	def addPlayer(self, name):
		# TODO: check for duplicates
		self.players[name] = Player(name, self.bounds)

	def drawSurface(self):
		surface = pygame.Surface((1024, 768))

		for key in self.players:
			# check for player collision
			for otherKey in self.players:
				if key != otherKey and self.players[otherKey].collidesWith(
					self.players[key].rects):
					self.players[key].kill()
					self.players[otherKey].kill()

			# make position updates to collition rectangles from velocity
			self.players[key].update()

			# draw all the rectangles
			#surface.blit(self.players[key].drawSurface(), (0,0))
			self.players[key].drawToSurface(surface)

		return surface
