import time

class RateLimiter:
	
	def __init__(self, limitPeriod):
		self.rateLimitQueue = {}
		self.limitPeriod = limitPeriod
		
	def isUserRateLimited(self, user):
		if user in self.rateLimitQueue:
			if time.mktime(time.gmtime()) > self.rateLimitQueue[user]:
				del self.rateLimitQueue[user]
			else:
				return True
		return False
		
	def limitUser(self, user):
		if user not in self.rateLimitQueue:
			self.rateLimitQueue[user] = time.mktime(time.gmtime()) + self.limitPeriod