#!/usr/bin/python
#coding:utf-8

# auth.py

# Import standard modules

import sha
import sqlite3


# Constants

NOTEXIST = 100
INCORRECTPASSWORD = 101
CORRECT = 102
EXIST = 103
DONE = 104


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
			return EXIST
		# Store entry in the database
		c = self.authdb.cursor()
		c.execute('insert into users values (\'%s\', \'%s\')' % (username,
				self.gethash(password)))
		self.authdb.commit()
		c.close()
		self.reload()
		return DONE

	def check(self, username, password):
		'''Checks if the user is registered in the database, and returns
		the appropriate response.'''
		if self.exists(username) == False:
			return NOTEXIST
		# Check for the correct password
		correct_password = False
		if self.db[username] == self.gethash(password):
			return CORRECT
		else:
			return INCORRECTPASSWORD
		

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
		return DONE

	def exists(self, username):
		'''Check if a user exists.'''
		exists = False
		for db_username in self.db:
			if username == db_username: exists = True
		return exists

	def gethash(self, what):
		return sha.new(what).hexdigest()

