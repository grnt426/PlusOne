import sys
import time
import logging
import logging.handlers 
from slackclient import SlackClient
import upvotehandler
import votehandler
import slackhelper

logger = logging.getLogger("plusone")
logger.setLevel(logging.DEBUG)
fh = logging.handlers.TimedRotatingFileHandler("history.log", when="D", interval=1, backupCount=3)
logger.addHandler(fh)


# Grab the API token to allow us to authenticate with Slack
data = sys.stdin.readlines()
if len(data) is not 1:
	print("Need the bot's User Token")
	sys.exit(1)
token = data[0]
logger.info("Token {}".format(token))

sc = SlackClient(token)
slack = slackhelper.SlackHelper(sc)
if sc.rtm_connect():

	payload = {}
	
	# Build the list of handlers, which will process all messages from Slack
	handlers = [upvotehandler.UpvoteHandler(slack), votehandler.VoteHandler(slack)]
	
	# Process forever
	while True:
		result = sc.rtm_read()
		if len(result) is 0:
			time.sleep(1)
			continue
		logger.debug("Data {}".format(result))
		for event in result:
			for handler in handlers:
				try:
					handler.handleEvent(event)
				except Exception as e:
					logger.error("Something happened to a handler :( {}".format(e))
					continue
else:
	print("Failed to connect :(")
	logger.error("Failed to connect")
	sys.exit(1)