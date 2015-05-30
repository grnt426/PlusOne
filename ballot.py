import logging

class Ballot:

	def __init__(self, helper, title, quorum, options, channel):
		self.title = title
		self.quorum = quorum
		self.votes = {}
		self.logger = logging.getLogger("plusone.Ballot")
		self.client = helper
		self.channel = channel
		self.options = options
		self.optionTally = {}
		self.concluded = False
	
	def recordVote(self, user, option):
		self.votes[user] = option
		if option not in self.optionTally:
			self.optionTally[option] = 0
		self.optionTally[option] = self.optionTally[option] + 1
		self.client.postMessage(self.channel, "{}\n{}".format(self.title, self.__str__()))
		return self.isConcluded()
		
	def isValidVote(self, user, option, channel):
		if user in self.votes:
			self.logger.debug("User already voted. Ignoring...")
			return False
		if channel != self.channel:
			self.logger.debug("Wrong channel...")
			return False
		if option not in self.options:
			self.logger.debug("Invalid option '{}'".format(option))
			return False
		return True
			
	def __str__(self):
		ballot = ">"
		for option, tally in self.optionTally.iteritems():
			ballot = "{}{}:{}  ".format(ballot, option, tally)
		return ballot
		
	def isConcluded(self):
		if len(self.votes) == self.quorum:
			self.concluded = True
		return self.concluded
		