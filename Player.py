import pygame

from random import *

class CollisionRect(pygame.Rect):
	def __init__(self, x, y, w, h, dx, dy):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.dx = dx
		self.dy = dy

	def update(self):
		self.x += self.dx
		self.y += self.dy

class Player(object):
	def __init__(self, name, bounds):
		self.name = name

		# init stats
		self.deaths = 0
		self.maxLen = 1

		self.newDx = 0
		self.newDy = 0

		self.bounds = bounds

		self.spawn()

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
			
	def spawn(self):
		x = randint(0, self.bounds.w - 25);
		x = x - (x % 25)
		y = randint(0, self.bounds.h - 25);
		y = y - (y % 25)

		# set velocity away from closes wall

		# determine if the top or bottom wall is closer than 
		# the left or right wall
		distLeftRight = min(self.bounds.w - x, x)
		distUpDown = min(self.bounds.h - y, y)

		dx = 0
		dy = 5
		if distLeftRight < distUpDown:
			dy = 0
			if x < self.bounds.w / 2:
				# move right
				dx = 5
			else:
				# move left
				dx = -5
		else:
			dx = 0
			if y < self.bounds.h / 2:
				# move down
				dy = 5
			else:
				dy = -5

		self.rects = [ CollisionRect(x,y,25,25,dx,dy) ]
	
	def kill(self):
		self.spawn()
		self.deaths += 1

	def eat(self):
		tail = self.rects[len(self.rects) - 1]

		# lengthen the tail in the appropriate direction
		# give new collision rectangle dx dy of last rect
		if tail.dx > 0:
			self.rects.append(CollisionRect(tail.x-25, tail.y,
				25, 25,
				tail.dx, tail.dy))
		elif tail.dx < 0:
			self.rects.append(CollisionRect(tail.x+25, tail.y,
				25, 25,
				tail.dx, tail.dy))
		elif tail.dy > 0:
			self.rects.append(CollisionRect(tail.x, tail.y-25,
				25, 25,
				tail.dx, tail.dy))
		elif tail.dy < 0:
			self.rects.append(CollisionRect(tail.x, tail.y+25,
				25, 25,
				tail.dx, tail.dy))

		# update longest personal record this game
		length = len(self.rects)
		if length > self.maxLen:
			self.maxLen = length

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
