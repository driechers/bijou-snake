import pygame

class collisionRect(object):
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.dx = 0
		self.dy = 0

	def update(self):
		self.x += self.dx
		self.y += self.dy

	def getRect(self):
		return pygame.Rect(x, y, w, h)

class Player(object):
	def __init__(self, name):
		self.name = name

		#going away soon
		self.length = 1
		self.x = 25
		self.y = 25

		self.rects = [ collisionRect(25,25,25,25) ]

	def update(self):
		for i,rect in enumerate(self.rects):
			self.rects[i].update()

	def setVelocity(self, dx, dy):
		self.rects[0].dx = dx
		self.rects[0].dy = dy

	def drawToSurface(self, surface):
		for rect in self.rects:
			pygame.draw.rect(surface, (255,255,255),
				(rect.x, rect.y, 25,25))
