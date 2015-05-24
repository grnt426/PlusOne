import logging

class UpvoteHandler:
	"""Searches messages for '++user', and gives them a +1"""
	
	def __init__(self, sc, usersList):
		self.client = sc
		self.users = usersList
		self.logger = logging.getLogger("UpvoteHandler")

	def handleEvent(self, event):
		
		if "type" not in event:
			self.logger.debug("Unknown message type, ignoring")
			return
		
		if event['type'] == "message":
			self.logger.debug("Found message")
			if 'channel' not in event:
				self.logger.debug("Not in a channel")
				return
			channel = event['channel']
			if "text" not in event:
				self.logger.debug("No text object? Skipping...")
				return
			text = event['text']
			if "++" in text:
				self.logger.debug("Plus one!")
				if text.index("++") != 0:
					self.logger.debug("Only support prefix notation!")
					return
				
				user = text[text.index("++")+2:]
				if user == "":
					self.logger.debug("User's name is empty???")
					return
				user = user.lower()
				self.logger.debug("User '{}'".format(user))
				
				if user not in self.users:
					self.logger.debug("Cannot find user, ignoring")
					return
					
				self.users[user] = self.users[user] + 1
				message = "{} + {}".format(user, self.users[user])
				self.logger.info(message)
				self.client.rtm_send_message(channel, message)