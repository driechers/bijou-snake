#!/usr/bin/python

import pygame
import math
import sys
import socket

from Map import Map
from JoinPage import JoinPage

from pygame.locals import *
from threading import Thread, Lock

bounds = (1024, 768)

JOIN = 0
PLAY = 1
SCORE = 2

class Game(object):
	def __init__(self):
		pygame.init()

		#self.screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode(bounds)
		self.clock = pygame.time.Clock()
		self.state = JOIN

		mapRect = pygame.Rect(0, 0, bounds[0], bounds[1])
		self.map = Map(mapRect)
		self.quit = False

		UDP_IP = "0.0.0.0"
		UDP_PORT = 5005

		self.sock = socket.socket(socket.AF_INET, # Internet
			socket.SOCK_DGRAM) # UDP
		self.sock.settimeout(.1)
		self.sock.bind((UDP_IP, UDP_PORT))

		pygame.mouse.set_visible(False)

		self.joinPage = JoinPage(bounds)

		self.mutex = Lock()
		t = Thread(target = Game.netThread, args = (self,))
		t.start()

		self.countDown()

	def countDown(self):
		self.joinPage.startCountDown(10)

		while True:
			self.mutex.acquire()
			if self.joinPage.ready:
				self.mutex.release()
				break

			self.screen.blit(self.joinPage.drawSurface(), (0,0))
			self.mutex.release()

			pygame.display.flip()

		self.play()

	def netThread(self):
		while True:
			# Check for quit
			self.mutex.acquire()
			if self.quit:
				self.map.destroy()
				self.mutex.release()
				break
			self.mutex.release()

			# handle single packet
			data = ''
			try:
				data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
			except socket.timeout:
				pass

			# parse packet data
			d = data.split(':')

			player = ''
			action = ''
			if len(d) == 2:
				player = d[0]
				action = d[1]

			# perform the action
			hor = 0
			vert = 0
			if self.state == PLAY:
				if action == 'left': hor = -5
				if action == 'right': hor = 5
				if action == 'up': vert = -5
				if action == 'down': vert = 5

			self.mutex.acquire()

			if action == 'join':
				if self.state == JOIN:
					self.map.addPlayer(player)
					self.joinPage.addPlayer(player)
			elif self.state == PLAY:
				try:
					self.map.players[player].setVelocity(hor, vert)
				except Exception:
					pass

			self.mutex.release()

	def play(self):
		self.state = PLAY

		while 1:
			# look for exit
			self.clock.tick(30)
			for event in pygame.event.get():
				if not hasattr(event, 'key'): continue
				if event.key == K_ESCAPE:
					self.mutex.acquire()
					self.quit = True
					self.mutex.release()

					sys.exit(0)

			# draw the screen
			self.mutex.acquire()
			self.screen.blit(self.map.drawSurface(), (0,0))
			self.mutex.release()
			
			pygame.display.flip()
 
if __name__ == "__main__":
	game = Game()
