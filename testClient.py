#!/usr/bin/python

import socket
import sys, tty, termios

def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

uid = "driechers"
action = "join"

print "sending join as " + uid

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.sendto(uid + ':' + action, (UDP_IP, UDP_PORT))

while(1):
	c = getch()

	if c == 'w': action = 'up'
	elif c == 'a': action = 'left'
	elif c == 's': action = 'down'
	elif c == 'd': action = 'right'
	elif c == 'q': break

	print action

	sock.sendto(uid + ':' + action, (UDP_IP, UDP_PORT))
