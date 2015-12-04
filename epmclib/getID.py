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
		self.singleresult = self.rawresults['resultList']['result'][0]

	def liteQuery(self):
		query = {'query':self.query, 'resulttype': 'lite', 'format': 'json'}
		r = requests.get(self.epmc_basequeryurl, params=query)
		self.rawresults = r.json()


	def getTitle(self):
		if self.resolves() == True:
			try:
				singleresult = self.rawresults['resultList']['result'][0]
				self.title=singleresult.get('title')
			except KeyError:
				self.title = ""
		else:
			raise(IDNotResolvedException)

	def getBBasicMetadata(self):
		self.coreQuery()
		if self.resolves() == True:
			singleresult = self.rawresults['resultList']['result'][0]
			metadata = {'authors' : list(), 'orcids': dict()}

			if not hasattr(self, 'title'):
				self.getTitle()
			metadata['title'] = self.title
			metadata['authors'] = [ author.get('fullName') for author in singleresult['authorList']['author'] ]
			metadata['date'] = singleresult.get('firstPublicationDate')
			metadata['volume'] = singleresult['journalInfo'].get('volume')
			metadata['issue'] = singleresult['journalInfo'].get('issue')
			metadata['pages'] = singleresult.get('pageInfo')
			metadata['journal'] = singleresult['journalInfo']['journal'].get('title')
			metadata['issn'] = singleresult['journalInfo']['journal'].get('issn')
			metadata['doi'] = singleresult.get('doi')
			metadata['pmid'] = singleresult.get('pmid')
			metadata['pmcid'] = singleresult.get('pmcid')



			self.metadata = metadata


