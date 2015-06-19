import json

class User:

	def __init__(self, userData):
		self.userData = userData
		self.id = userData['id']
		self.username = userData['name']
		
		self.profileData = userData['profile']
		if 'first_name' in self.profileData:
			self.firstName = self.profileData['first_name']
		else:
			self.firstName = ""
		if 'last_name' in self.profileData:
			self.lastName = self.profileData['last_name']
		else:
			self.lastName = ""
		
	def getFirstName(self):
		return self.firstName
		
	def getLastName(self):
		return self.lastName
		
	def getUsername(self):
		return self.username
	
	def getUserId(self):
		return self.id
		
	def getUserData(self, data):
		return self.userData[data]
		
	def getProfileData(self, data):
		return self.profileData[data]