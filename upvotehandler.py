import logging
import string
import ratelimiter

class UpvoteHandler:
	"""Searches messages for '++user', and gives them a +1"""
	
	def __init__(self, helper):
		self.client = helper
		self.users = helper.getUsers()
		self.logger = logging.getLogger("plusone.UpvoteHandler")
		self.RESULT_FILE = "tallies.txt"
		self.retrieveSavedData()
		self.rateLimiter = ratelimiter.RateLimiter(60) # Limit to 1/min

	def handleEvent(self, event):
		
		if self.canHandle(event):
			self.logger.debug("Plus one!")
			channel = event['channel']
			text = event['text']
			user = self.parseUser(text)
			if user is None:
				self.logger.debug("No user found for ++")
				return

			if self.rateLimiter.isUserRateLimited(user):
				self.logger.debug("User was rate limited")
				return
			self.rateLimiter.limitUser(user)
			
			self.users[user] = self.users[user] + 1
			message = "{} + {}".format(user, self.users[user])
			self.writeCurrentResults()
			self.logger.info("{}: {}".format(channel, message))
			self.client.postMessage(channel, message)
	
	def canHandle(self, event):
		if "type" not in event:
			self.logger.debug("Unknown message type, ignoring")
			return False
		
		if event['type'] == "message":
			self.logger.debug("Found message")
			if 'channel' not in event:
				self.logger.debug("Not in a channel")
				return False
			if "text" not in event:
				self.logger.debug("No text object? Skipping...")
				return False
			text = event['text']
			if "++" in text:
				return True
		return False
		
	def parseUser(self, text):
		user = ""
		text = text.partition("++")
		
		# Check if the name is in front of the ++
		if text[0] != "" and " " not in text[0]:
			user = text[0]
		elif text[0] != "" and " " in text[0]:
			user = text[0][text[0].rindex(" ")+1:]
			
		exclude = set(string.punctuation)
		user = ''.join(ch for ch in user if ch not in exclude)
		
		# If we didn't find it, then check if the name is behind the ++
		if user == "":
			if text[2] != "" and " " not in text[2]:
				user = text[2]
			elif text[2] != "" and " " in text[2]:
				user = text[2][:text[2].index(" ")]
				
		exclude = set(string.punctuation)
		user = ''.join(ch for ch in user if ch not in exclude)
		
		if user == "":
			self.logger.debug("User's name is empty???")
			return None
		
		user = user.lower()
		self.logger.debug("User '{}'".format(user))
		
		if user not in self.users:
			self.logger.debug("Cannot find user, ignoring")
			return None
		return user
			
	def writeCurrentResults(self):
		resultStr = ""
		for user, count in self.users.iteritems():
			if count == 0:
				continue
			resultStr = "{}{},{}\n".format(resultStr, user, count)
		save = open(self.RESULT_FILE, "w")
		save.write(resultStr)
		save.close()
		
	def retrieveSavedData(self):
		saved = open(self.RESULT_FILE, "r")
		for line in saved:
			data = line.split(",")
			self.users[data[0]] = int(data[1])
		saved.close()
			