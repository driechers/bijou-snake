#!/usr/bin/python

import pygame
import math
import sys

import socket

from Map import Map
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255, 255, 255)

class Game(object):
	def __init__(self):
		#self.screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode((1024, 768))
		self.clock = pygame.time.Clock()
		self.map = Map()

		UDP_IP = "127.0.0.1"
		UDP_PORT = 5005

		self.sock = socket.socket(socket.AF_INET, # Internet
			socket.SOCK_DGRAM) # UDP
		self.sock.settimeout(.2)
		self.sock.bind((UDP_IP, UDP_PORT))

		pygame.mouse.set_visible(False)
		self.run()

	def run(self):
		while 1:
			# look for exit
			self.clock.tick(30)
			for event in pygame.event.get():
				if not hasattr(event, 'key'): continue
				if event.key == K_ESCAPE: sys.exit(0)

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
			if action == 'left': hor = -25
			if action == 'right': hor = 25
			if action == 'up': vert = -25
			if action == 'down': vert = 25
			if action == 'join': self.map.addPlayer(player)

			try:
				self.map.players[player].x += hor
				self.map.players[player].y += vert
			except Exception:
				pass

			# draw the screen
			self.screen.blit(self.map.drawSurface(), (0,0))
			pygame.display.flip()
 
if __name__ == "__main__":
	game = Game()
