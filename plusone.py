import asyncio
import websockets
import requests
import json

@asyncio.coroutine
def hello(socketUrl, channels):
	print("URL {}".format(socketUrl))
	websocket = yield from websockets.connect(socketUrl)
	while True:
		result = yield from websocket.recv()
		print("Data {}".format(result))
		data = json.loads(result)
		if data['type'] == "message":
			print("Found message")
			channel = data['channel']
			text = data['text']
			if "grant++" in text:
				print("Plus one!")
				postData = "Grant was just incremented"
				responseUrl = 'https://nhstechteam.slack.com/services/hooks/slackbot?token=xTb8jdy1oJFdFbqMchjMEcHO&channel=%23general'
				print("Response: {}".format(responseUrl))
				r = requests.post(responseUrl, postData)
				print("Response: {}".format(r.text))

r = requests.get('https://slack.com/api/rtm.start?token=xoxp-4997715752-5022309795-5001368532-4f2da6')
data = r.json()
socketUrl = data['url']
channels = data['channels']

asyncio.get_event_loop().run_until_complete(hello(socketUrl))
