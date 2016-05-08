#!/usr/bin/python

import pygame
import math
import sys
import socket

from Map import Map
from pygame.locals import *
from threading import Thread, Lock

class Game(object):
	def __init__(self):
		#self.screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode((1024, 768))
		self.clock = pygame.time.Clock()
		self.map = Map()
		self.quit = False

		UDP_IP = "127.0.0.1"
		UDP_PORT = 5005

		self.sock = socket.socket(socket.AF_INET, # Internet
			socket.SOCK_DGRAM) # UDP
		self.sock.settimeout(.1)
		self.sock.bind((UDP_IP, UDP_PORT))

		pygame.mouse.set_visible(False)

		self.mutex = Lock()
		t = Thread(target = Game.netThread, args = (self,))
		t.start()

		self.run()

	def netThread(self):
		while True:
			# Check for quit
			self.mutex.acquire()
			if self.quit:
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
			if action == 'left': hor = -5
			if action == 'right': hor = 5
			if action == 'up': vert = -5
			if action == 'down': vert = 5

			self.mutex.acquire()

			if action == 'join':
				self.map.addPlayer(player)
			else:
				try:
					self.map.players[player].setVelocity(hor, vert)
				except Exception:
					pass

			self.mutex.release()

	def run(self):
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
