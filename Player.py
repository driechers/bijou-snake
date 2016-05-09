import pygame

from random import *

class CollisionRect(pygame.Rect):
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

class Player(object):
	def __init__(self, name, bounds):
		self.name = name

		self.newDx = 0
		self.newDy = 0

		self.bounds = bounds

		self.rects = [ CollisionRect(25,25,25,25) ]

		self.tick = 0

	def inBounds(self):
		for rect in self.rects:
			if not self.bounds.contains(rect):
				return False

		return True

	def collidesWithSelf(self):
		head = self.rects[0]

		for i, rect in enumerate(self.rects):
			if i > 1 and head.colliderect(rect):
				return True

		return False

	def collidesWith(self, other):
		for otherRect in other:
			for rect in self.rects:
				if otherRect.colliderect(rect):
					return True

		return False
			

	def kill(self):
		x = randint(0, self.bounds.w - 25);
		x = x - (x % 25)
		y = randint(0, self.bounds.h - 25);
		y = y - (y % 25)

		self.rects = [ CollisionRect(x,y,25,25) ]

	def eat(self):
		tail = self.rects[len(self.rects) - 1]

		if tail.dx > 0:
			self.rects.append(CollisionRect(tail.x-25, tail.y, 25, 25))
		elif tail.dx < 0:
			self.rects.append(CollisionRect(tail.x+25, tail.y, 25, 25))
		elif tail.dy > 0:
			self.rects.append(CollisionRect(tail.x, tail.y-25, 25, 25))
		elif tail.dy < 0:
			self.rects.append(CollisionRect(tail.x, tail.y+25, 25, 25))

		self.rects[len(self.rects) - 1].dx = tail.dx
		self.rects[len(self.rects) - 1].dy = tail.dy

	def update(self):
		# kill if out of bounds
		if not self.inBounds():
			self.kill()

		# kill if colliding with self
		if self.collidesWithSelf():
			self.kill()

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
