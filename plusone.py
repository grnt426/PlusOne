import asyncio
import websockets
import requests
import json

@asyncio.coroutine
def hello(socketUrl, channels, users):
	print("URL {}".format(socketUrl))
	websocket = yield from websockets.connect(socketUrl)
	while True:
		result = yield from websocket.recv()
		print("Data {}".format(result))
		data = json.loads(result)
		if data['type'] == "message":
			print("Found message")
			channel = channels[data['channel']]
			text = data['text']
			if "++" in text:
				print("Plus one!")
				user = text[text.index("++")+2:]
				print("User '{}'".format(user))
				users[user] = users[user] + 1
				print("Incrementing {} to {}".format(user, users[user]))
				postData = "{} + {}".format(user, users[user])
				responseUrl = 'https://nhstechteam.slack.com/services/hooks/slackbot?token=xTb8jdy1oJFdFbqMchjMEcHO&channel=%23' + channel
				print("Response: {}".format(responseUrl))
				r = requests.post(responseUrl, postData)
				print("Response: {}".format(r.text))

r = requests.get('https://slack.com/api/rtm.start?token=xoxp-4997715752-5022309795-5001368532-4f2da6')
data = r.json()
socketUrl = data['url']

rawChannels = data['channels']
channels = {}
for channel in rawChannels:
	channels[channel['id']] = channel['name']

rawUsers = data['users']
users = {}
for user in rawUsers:
	name = user['profile']['first_name'].lower()
	print("User: {}".format(name))
	users[name] = 0
	
asyncio.get_event_loop().run_until_complete(hello(socketUrl, channels, users))
