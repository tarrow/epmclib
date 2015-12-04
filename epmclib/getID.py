import requests
import requests_cache
from . exceptions import IDNotResolvedException

class getID():
	epmc_basequeryurl = "http://www.ebi.ac.uk/europepmc/webservices/rest/search"
	requests_cache.install_cache(cache_name='epmc_cache', expire_after=2.628*10**6)

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
		r = requests.get(self.epmc_basequeryurl, params=webquery)
		self.rawresults = r.json()

	def liteQuery(self):
		query = {'query':self.query, 'resulttype': 'lite', 'format': 'json'}
		r = requests.get(self.epmc_basequeryurl, params=query)
		self.rawresults = r.json()

	def getTitle(self):
		self.liteQuery()
		if self.resolves() == True:
			try:
				self.title=self.rawresults['resultList']['result'][0]['title']
			except KeyError:
				self.title=""
		else:
			raise(IDNotResolvedException)

	def getLBMetadata(self):
		self.coreQuery()
		if self.resolves() == True:
			metadata = {'authors' : list(), 'orcids': dict()}
			metadata['authors'].append(self.rawresults.get())

