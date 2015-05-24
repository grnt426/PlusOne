import sys
import time
import json
import upvotehandler
import logging
from slackclient import SlackClient

logging.basicConfig(filename='history.log',filemode='w',level=logging.DEBUG)

def processUsers(data):
	data = json.loads(data)
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
	return users

# Grad the API token to allow us to authenticate with Slack
data = sys.stdin.readlines()
if len(data) is not 1:
	print("Need the bot's User Token")
	sys.exit(1)
token = data[0]
logging.info("Token {}".format(token))

sc = SlackClient(token)
if sc.rtm_connect():

	payload = {}
	users = processUsers(sc.api_call("users.list"))

	# Build the list of handlers, which will process all messages from Slack
	handlers = [upvotehandler.UpvoteHandler(sc, users)]
	
	# Process forever
	while True:
		result = sc.rtm_read()
		if len(result) is 0:
			time.sleep(1)
			continue
		logging.debug("Data {}".format(result))
		for event in result:
			for handler in handlers:
				try:
					handler.handleEvent(event)
				except Exception as e:
					logging.error("Something happened to a handler :(: {}".format(e))
					continue
else:
	print("Failed to connect :(")
	logging.error("Failed to connect")
	sys.exit(1)