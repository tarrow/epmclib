import requests

class getID():
	epmc_basequeryurl = "http://www.ebi.ac.uk/europepmc/webservices/rest/search"

	def __init__(self, id):
		self.id = id

	def resolves(self):
		self.liteQuery()
		if self.results['hitCount'] == 1:
			return True
		else:
			return False

	def coreQuery(self):
		query = {'query':self.id,'resulttype':'core', 'format':'json'}
		self.results = requests.get(epmc_basequeryurl, params=query)

	def liteQuery(self):
		query = {'query':self.id,'resulttype':'lite', 'format':'json'}
		r = requests.get(self.epmc_basequeryurl, params=query)
		self.results = r.json()