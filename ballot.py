import logging

class Ballot:

	def __init__(self, sc, title, quorum, options, channel):
		self.title = title
		self.quorum = quorum
		self.votes = {}
		self.logger = logging.getLogger("Ballot")
		self.client = sc
		self.channel = channel
		self.options = options
		self.optionTally = {}
		self.concluded = False
	
	def recordVote(self, user, option):
		self.votes[user] = option
		if option not in self.optionTally:
			self.optionTally[option] = 0
		self.optionTally[option] = self.optionTally[option] + 1
		self.printBallot()	
		
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
			
	def printBallot(self):
		ballot = ">"
		for option, tally in self.optionTally.iteritems():
			ballot = "{}{}:{}  ".format(ballot, option, tally)
		self.client.rtm_send_message(self.channel, "{}\n{}".format(self.title, ballot))
		
	def isConcluded(self):
		return self.concluded
		