import requests

class getID():
	epmc_basequeryurl = "http://www.ebi.ac.uk/europepmc/webservices/rest/search"

	def __init__(self, id):
		self.query = id

	def resolves(self):
		if not hasattr(self, 'rawresults'):
			self.liteQuery()
		if self.rawresults['hitCount'] == 1:
			return True
		else:
			return False

	def coreQuery(self):
		webquery = {'query':self.query, 'resulttype': 'core', 'format': 'json'}
		self.rawresults = requests.get(epmc_basequeryurl, params=webquery)

	def liteQuery(self):
		query = {'query':self.query, 'resulttype': 'lite', 'format': 'json'}
		r = requests.get(self.epmc_basequeryurl, params=query)
		self.rawresults = r.json()

	def getTitle(self):
		self.liteQuery()
		if self.resolves() == True:
			self.title=self.rawresults['resultList']['result'][0]['title']
