import logging
import string
import ratelimiter

class UpvoteHandler:
	"""Searches messages for '++user', and gives them a +1"""
	
	def __init__(self, helper):
		self.client = helper
		self.scores = {}
		self.logger = logging.getLogger("plusone.UpvoteHandler")
		self.RESULT_FILE = "tallies.txt"
		self.retrieveSavedData()
		self.rateLimiter = ratelimiter.RateLimiter(15) # Limit to 4/min

	def handleEvent(self, event):
		
		if self.canHandle(event):
			self.logger.debug("Plus one!")
			channel = event['channel']
			text = event['text']
			user = self.parseUser(text, channel)
			if isinstance(user, list):
				self.logger.debug("User matches multiple people")
				self.client.postMessage(channel, "Sorry, that matches multiple people. Try another name (or username).")
				return
			if user is None:
				self.logger.debug("No user found for ++")
				return
			
			userId = user.getUserId()
			self.logger.debug("User ID: {}".format(userId))
			if self.rateLimiter.isUserRateLimited(userId):
				self.logger.debug("User was rate limited")
				return
			self.rateLimiter.limitUser(userId)
			self.logger.debug("User not rate limited")

			if userId in self.scores:
				self.scores[userId] = self.scores[userId] + 1
			else:
				self.scores[userId] = 1

			message = "{} + {}".format(user.getUsername(), self.scores[userId])
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
		
	def parseUser(self, text, channel):
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
		
		matchedUser = self.client.findUserMatch(user)
		self.logger.debug("Matched User '{}'".format(matchedUser))
		return matchedUser
			
	def writeCurrentResults(self):
		resultStr = ""
		for user, count in self.scores.iteritems():
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
			self.scores[data[0]] = int(data[1])
		saved.close()
			