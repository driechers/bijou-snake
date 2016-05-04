import pygame
from Player import Player

class Map(object):

	def __init__(self):
		p1 = Player("Player 1")
		p2 = Player("Player 2")
		self.players = [ p1, p2 ]
		self.player = 0

	def getPlayer(self):
		ret = self.player
		self.player = (self.player + 1) % len(self.players)

		return ret

	def drawSurface(self):
		surface = pygame.Surface((1024, 768))

		for player in self.players:
			pygame.draw.rect(surface, (255,255,255),
				(player.x, player.y, 25,25))

		return surface
