#!/usr/bin/python
#coding:utf-8

# server.py

# Import standard modules
import socket

def process(self, socket_info):
	'''Process the socket.'''
	(socket, port) = socket_info
	while 1:
		readbuffer = ''
		# Wait for them to send data.
		readbuffer = readbuffer + socket.recv(512)
		# Close the socket if they don't send anything.
		if not len(readbuffer):
			break
		# Does the data end with ;
		if readbuffer[len(readbuffer)-1:len(readbuffer)] != ';':
			(username, password) = readbuffer.split(':')
			print password
			password = password[:len(password)-1]
			print password
			import auth
			a = auth.Auth('authdb'); a.reload()
			check = a.check(username, password[:len(password)-1])
			print check
			if check == (auth.NOTEXIST or auth.INCORRECTPASSWORD):
				socket.send('N')
			elif check == (auth.CORRECT):
				socket.send('Y')
			else:
				socket.send('N')

# Main code

class Server:
	socket = None
	addr = None

	def __init__(self, addr):
		self.addr = addr
		# Create a socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Try to bind the socket, unless stupid users don't know how to specify addresses, then complain and crash their program
		try: self.socket.bind(self.addr)
		except TypeError: print 'Please specify addr in this form: (hostname[str], port[int]).'; exit()
		# Listen on the socket
		self.socket.listen(5) # I don't know what the 5 is.

	def poll(self):
		'''Wait for somebody to connect, and send their connection if they do.'''
		# Wait for somebody to connect
		while 1:
			# Accept a socket
			socket_info = self.socket.accept()
			process(socket_info) # This is only here until I write the real server code.

