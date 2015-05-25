import logging
import json

class SlackHelper:

	def __init__(self, sc):
		self.client = sc
		self.rawUsers = sc.api_call("users.list")
		self.logger = logging.getLogger("SlackHelper")
		self.users = {}
		self.userIds = {}
		
	def getUsers(self):
		if len(self.users) != 0:
			return self.users
			
		data = json.loads(self.rawUsers)
		logging.debug("processing users {}".format(data["members"]))
		users = {}
		for user in data["members"]:
			logging.debug("Raw {}".format(user))
			profile = user['profile']
			if 'first_name' not in profile:
				logging.debug("Skipping user...")
				continue
			name = profile['first_name'].lower()
			logging.info("User: {}".format(name))
			users[name] = 0
		self.users = users
		return users
		
	# This is really lazy, consolidate later...
	def getUserIds(self):
		if len(self.userIds) != 0:
			return self.userIds
	
		data = json.loads(self.rawUsers)
		users = {}
		for user in data["members"]:
			if 'first_name' not in user['profile']:
				continue
			else:
				users[user['id']] = user['profile']['first_name']
		self.userIds = users
		return users
		
	def postMessage(self, channel, message):
		""" Handles posting to both public channels and private groups """
		channel = self.client.server.channels.find(channel)
		if channel is not None:
			channel.send_message(message)
		else:
			self.logger.error("Can't find channel")