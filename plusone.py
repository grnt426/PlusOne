import sys
import time
import json
from slackclient import SlackClient

def handleEvent(event, users, sc):
	print("Event {}".format(event))
	if "type" not in event:
		print("Unknown message type, ignoring")
		return
		
	if event['type'] == "message":
		print("Found message")
		if 'channel' not in event:
			print("Not in a channel")
			return
		channel = event['channel']
		if "text" not in event:
			print("No text object? Skipping...")
			return
		text = event['text']
		if "++" in text:
			print("Plus one!")
			if text.index("++") != 0:
				print("Only support prefix notation!")
				return
			
			user = text[text.index("++")+2:]
			if user == "":
				print("User's name is empty???")
				return
			user = user.lower()
			print("User '{}'".format(user))
			
			if user not in users:
				print("Cannot find user, ignoring")
				return
				
			users[user] = users[user] + 1
			message = "{} + {}".format(user, users[user])
			print(message)
			sc.rtm_send_message(channel, message)

def processUsers(data):
	data = json.loads(data)
	print("processing users {}".format(data["members"]))
	users = {}
	for user in data["members"]:
		print("Raw {}".format(user))
		profile = user['profile']
		if 'first_name' not in profile:
			print("Skipping user...")
			continue
		name = profile['first_name'].lower()
		print("User: {}".format(name))
		users[name] = 0
	return users

data = sys.stdin.readlines()
if len(data) is not 1:
	print("Need the bot's User Token")
	sys.exit(1)
	
token = data[0]
print("Token {}".format(token))
sc = SlackClient(token)
if sc.rtm_connect():

	payload = {}
	users = processUsers(sc.api_call("users.list"))

	# All other reads will be events from Slack
	while True:
		result = sc.rtm_read()
		if len(result) is 0:
			time.sleep(1)
			continue
		print("Data {}".format(result))
		for event in result:
			handleEvent(event, users, sc)
else:
	print("Failed to connect :(")