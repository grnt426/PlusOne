import logging
import ballot

class VoteHandler:

	def __init__(self, helper):
		self.client = helper
		self.ballots = []
		self.currentChannel = "" # This is safe, as all operations are serialized
		self.logger = logging.getLogger("plusone.VoteHandler")
		self.userIds = helper.getUserIds()
	
	def handleEvent(self, message):
		if self.canHandle(message):
			self.currentChannel = message['channel']
			text = message['text']
			data = text.split(" ")
			user = message['user']
			
			if "callvote" in text:
				self.initiateVote(text)
			elif "makevote" in data:
				self.placeVote(data, user)
			elif "printvotes" in data:
				self.printCurrentResults(data)
			elif "printballots" in data:
				self.printCurrentBallots()
			elif "finishvote" in data:
				self.concludeVoting(data)
			elif "helpvote" in data:
				self.voteHelp()
		
	def canHandle(self, event):
		if "type" not in event:
			self.logger.debug("Unknown message type, ignoring")
			return False
		
		if event['type'] == "message":
			self.logger.debug("Found message")
			if "channel" not in event:
				self.logger.debug("Not in a channel")
				return False
			if "text" not in event:
				self.logger.debug("No text object? Skipping...")
				return False
			return True
		return False
		
	def initiateVote(self, message):
		"""
			Starts a vote, with the default of binary yes/no for options
			Format: callvote [title] [votes] (options)
		"""
		
		# The command itself counts towards the total
		if len(message) < 3:
			self.client.postMessage(self.currentChannel, "Invalid format for callvote, Expected callvote |[title]| [votes] (options)")
		
		title = message[message.index("|")+1:message.rindex("|")]
		if title == "":
			self.client.postMessage(self.currentChannel, "Empty title? :\\")
			return
		
		if message.rindex("|") == len(message) - 1:
			self.client.postMessage(self.currentChannel, "Invalid format for callvote, Expected callvote |[title]| [votes] (options)")
	
		message = message[message.rindex("|") + 1:]
		self.logger.debug("Options: {}".format(message))
		message = message.split(" ")
		votes = 0
		try:
			votes = int(message[1])
		except Exception:
			self.client.postMessage(self.currentChannel, "Invalid format for callvote, Expected a number following the title for quorum.")
			return
		
		ballotForm = ballot.Ballot(self.client, title, votes, ("yea", "nay"), self.currentChannel)
		self.ballots.append(ballotForm)
		self.logger.debug("Title: {} Quorum: {}".format(title, votes))
		self.client.postMessage(self.currentChannel, "Vote for '{}' has started! {} votes are needed for quorum. 'makevote {} [yea | nay]' to vote.".format(title, votes, len(self.ballots) - 1))
	
	def placeVote(self, message, user):
		if len(message) < 3 or len(message) > 4:
			self.client.postMessage(self.currentChannel, "Invalid format for makevote, Expected makevote [voteid] [option]")
		
		if user not in self.userIds:
			self.logger.debug("User not bound to ID?")
		userName = self.userIds[user]
		
		ballotId = message[1]
		self.logger.debug("{} {} {}".format(user, ballotId, message[2]))
		
		if ballotId.isdigit:
			ballotId = int(ballotId)
		else:
			self.logger.debug("Invalid ballot ID")
			self.client.postMessage(self.currentChannel, "Invalid ballot ID.")
			
		if ballotId > len(self.ballots) - 1 or ballotId < 0:
			self.logger.debug("Ballot ID not found.")
			self.client.postMessage(self.currentChannel, "Ballot ID not found.")
			return
			
		ballotId = int(ballotId)
		ballotForm = self.ballots[ballotId]
		
		if ballotForm.isConcluded():
			self.logger.debug("Vote has already concluded.")
			return
		
		if ballotForm.isValidVote(user, message[2], self.currentChannel):
			self.logger.debug("Recording vote.")
			if ballotForm.recordVote(user, message[2]):
				self.concludeVoting(ballotForm)
		else:
			self.logger.debug("Vote not valid")

	def concludeVoting(self, ballotForm):
		self.logger.info("Ballot '{}' has concluded. Results: {}".format(ballotForm.title, ballotForm))
		self.client.postMessage(self.currentChannel, ">'{}' has concluded.".format(ballotForm.title))

	def printCurrentResults(self, ballotForm):
		return

	def printCurrentBallots(self):
		return
	
	def voteHelp(self):
		self.client.postMessage(self.currentChannel, "Format: callvote [title] [votes] (options). By default, only options are yea/nay. Separate options by commas. To place a vote: 'makevote [ballotid] [option]'")