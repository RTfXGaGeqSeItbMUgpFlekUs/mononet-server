#!/usr/bin/python
#coding:utf-8

# auth.py

# Import standard modules

import sha
import sqlite3


# Constants

AUTH_NOTEXIST = 100
AUTH_INCORRECTPASSWORD = 101
AUTH_CORRECT = 102
AUTH_EXIST = 103
AUTH_DONE = 104


# Main code

class Auth:
	authdb_file = ''
	authdb = None
	db = {}

	def __init__(self, authdb):
		self.authdb = sqlite3.connect(authdb)

	def register(self, username, password):
		'''Register the user in the database.'''
		if self.exists(username) == True:
			return AUTH_EXIST
		# Store entry in the database
		c = self.authdb.cursor()
		c.execute('insert into users values (\'%s\', \'%s\')' % (username,
				self.gethash(password)))
		self.authdb.commit()
		c.close()
		self.reload()
		return AUTH_DONE

	def check(self, username, password):
		'''Checks if the user is registered in the database, and returns
		the appropriate response.'''
		if self.exists(username) == False:
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
		# Get entries
		c = self.authdb.cursor()
		c.execute('select * from users')
		entries = c.fetchall()
		c.close()
		# Fill the database
		for entry in entries:
			username = entry[0]
			password = entry[1]
			# Set the passwords
			self.db[username] = password
		return AUTH_DONE

	def exists(self, username):
		'''Check if a user exists.'''
		exists = False
		for username in self.db:
			if username == username: exists = True
		return exists

	def gethash(self, what):
		return sha.new(what).hexdigest()

