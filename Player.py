import pygame

class collisionRect(object):
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.dx = 5
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
		self.newDx = 0
		self.newDy = 0

		self.rects = [ collisionRect(100,25,25,25), collisionRect(75,25,25,25) , collisionRect(50,25,25,25) , collisionRect(25,25,25,25) ]

		self.tick = 0

	def update(self):
		# every so often shift velocities to next block
		head = self.rects[0]

		# 25 to be replaced with width, height
		if ((head.x % 25) == 0 and head.dx) or ((head.y % 25) == 0 and head.dy):
			# update body velocity
			for i, rect in reversed(list(enumerate(self.rects))):
				if i != 0:
					self.rects[i].dx = self.rects[i-1].dx
					self.rects[i].dy = self.rects[i-1].dy

			# update head velocity once in valid spot
			if self.newDx or self.newDy:
				self.rects[0].dx = self.newDx
				self.rects[0].dy = self.newDy

				self.newDx = 0
				self.newDy = 0
				

		# update position of each rect
		for i,rect in enumerate(self.rects):
			self.rects[i].update()

	def setVelocity(self, dx, dy):
		head = self.rects[0]

		# do not allow reverse
		if (dx and head.dx != -dx) or (dy and head.dy != -dy):
			self.newDx = dx
			self.newDy = dy

	def drawToSurface(self, surface):
		for rect in self.rects:
			pygame.draw.rect(surface, (255,255,255),
				(rect.x, rect.y, 25,25))
