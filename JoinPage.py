import pygame
import time

class JoinPage(object):

	def __init__(self, bounds):
		self.playerNames = []

		self.bounds = bounds

		self.ready = False
		self.startTime = 0
		self.numSec = 0
		self.totalSec = 0

	def startCountDown(self, numSec):
		self.numSec = numSec
		self.totalSec = numSec

		self.startTime = time.time()

	def updateCountDown(self):
		self.numSec = int(round(self.totalSec - (time.time() - self.startTime)))

		if self.numSec <= 0:
			self.ready = True

	def addPlayer(self, name):
		self.playerNames.append(name)

	def drawSurface(self):
		surface = pygame.Surface(self.bounds)

		# draw players heading
		headingX = 50
		font = pygame.font.Font(None, 42)
		text = font.render("Players", 1, (255,255,255))
		surface.blit(text, (headingX, 100))

		headCenterX = text.get_rect().centerx

		y = 140
		for name in self.playerNames:
			font = pygame.font.Font(None, 23)
			text = font.render(name, 1, (255,255,255))

			nameW = text.get_rect().w
			surface.blit(text, (headCenterX - nameW/2 + headingX, y))

			y += 25

		self.updateCountDown()

		#draw countdown
		headingX = surface.get_rect().centerx
		headingY = surface.get_rect().centery - 40

		font = pygame.font.Font(None, 60)
		text = font.render("Game Starts In", 1, (255,255,255))
		textW = text.get_rect().w
		headingX = headingX - textW/2
		surface.blit(text, (headingX, headingY))

		headCenterX = text.get_rect().centerx

		font = pygame.font.Font(None, 42)
		text = font.render(str(self.numSec), 1, (255,255,255))

		textW = text.get_rect().w
		surface.blit(text, (headCenterX - textW/2 + headingX,
			headingY + 40))

		return surface
