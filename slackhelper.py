import logging
import json
import user

class SlackHelper:

	def __init__(self, sc):
		self.client = sc
		self.rawUsers = sc.api_call("users.list")
		self.logger = logging.getLogger("plusone.SlackHelper")
		self.users = {}
		self.userIds = []
		self.names = {}
		self.usernames = {}
		self.processUsers(self.rawUsers)
		
	def processUsers(self, rawUsers):
		data = json.loads(self.rawUsers)
		self.logger.debug("processing users {}".format(data["members"]))
		for userData in data["members"]:
			id = userData['id']
			self.userIds.append(id)
			username = userData['name']
			self.users[id] = user.User(userData)
			
			profile = userData['profile']
			if 'first_name' in profile:
				firstName = profile['first_name'].lower()
				self.addIfUnique(self.names, firstName, id)
			if 'last_name' in profile:
				lastName = profile['last_name'].lower()
				self.addIfUnique(self.names, lastName, id)
			if 'first_name' in profile and 'last_name' in profile:
				firstName = profile['first_name'].lower()
				lastName = profile['last_name'].lower()
				firstCompoundName = firstName + lastName[:1]
				lastCompoundName = lastName + firstName[:1]
				self.addIfUnique(self.names, firstCompoundName, id)
				self.addIfUnique(self.names, lastCompoundName, id)
				
			self.usernames[username] = id
			
	def addIfUnique(self, map, key, value):
		""" If it is already in the map, then we have a collision, and will
			resort to a list of IDs it could match on (for error reporting to the user) """ 
		if key in map:
			if isinstance(map[key], list):
				map[key].append(value)
			else:
				prevId = map[key]
				map[key] = [prevId, value]
		else:
			map[key] = value
		
	def getUsers(self):
		return self.users
		
	def getUserIds(self):
		return self.userIds
		
	def getUser(self, id):
		return self.users[id]
		
	def findUserMatch(self, term):
		id = -1
		if term in self.names:
			id = self.names[term]
		if term in self.usernames:
			id = self.usernames[term]
		
		if id == -1:
			return None
		if isinstance(id, list):
			return id
		else:
			return self.users[id]
		
	def postMessage(self, channel, message):
		""" Handles posting to both public channels and private groups """
		channel = self.client.server.channels.find(channel)
		if channel is not None:
			channel.send_message(message)
		else:
			self.logger.error("Can't find channel")