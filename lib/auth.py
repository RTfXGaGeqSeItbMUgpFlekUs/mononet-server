#!/usr/bin/python
#coding:utf-8

# auth.py

# Import standard modules

import sha


# Constants

AUTH_NOTEXIST = 100
AUTH_INCORRECTPASSWORD = 101
AUTH_CORRECT = 102


# Main code

class Auth:
	authdb_file = ''
	authdb = None
	db = {}

	def __init__(self, authdb):
		self.authdb_file = authdb
		self.authdb = open(self.authdb_file, 'r+a')
		self.reload()

	def register(self, username, password):
		'''Register the user in the database.'''
		# Create a database entry
		entry = '%s:%s;' % (username, self.gethash(password))
		# Store entry in the database
		self.authdb.write(entry)
		self.authdb.flush()

	def check(self, username, password):
		'''Checks if the user is registered in the database, and returns
		the appropriate response.'''
		# Check if the user exists
		exists = False
		for username in self.db:
			if username == username: exists = True
		if exists == False:
			return AUTH_NOTEXIST
		# Check for the correct password
		correct_password = False
		if self.db[username] == self.gethash(password):
			return AUTH_CORRECT
		else:
			return AUTH_INCORRECTPASSWORD
		

	def reload(self):
		'''Reloads the database.'''
		# Clear the database
		self.db = {}
		# Reload the file
		self.close()
		self.authdb = open(self.authdb_file, 'r+a')
		content = self.authdb.read()
		# Get entries
		entries = content.split(';')
		entries = entries[:len(entries)-1]
		for entry in entries:
			username = entry.split(':')[0]
			password = entry.split(':')[1]
			# Set the passwords
			self.db[username] = password

	def gethash(self, what):
		return sha.new(what).hexdigest()

	def close(self):
		self.authdb.close()

