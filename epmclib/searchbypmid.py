import requests, untangle

def searchByPMCid(pmcid):
	epmc_basequeryurl = "http://www.ebi.ac.uk/europepmc/webservices/rest/search"

	if pmcid[:3] != 'PMC':
		pmcid = 'PMCID:PMC' + pmcid
	else:
		pmcid = 'PMCID:' + pmcid

	''' Make query to EuropePMC'''
	query = {'query':pmcid,'resulttype':'core'}

	r = requests.get(epmc_basequeryurl, params=query)

	'''Use untangle to make python structure from xml'''
	obj = untangle.parse(r.text)

	'''test the it is ok result i.e. only one result and that is a journal article'''
	if not obj.responseWrapper.hitCount.cdata == '1':
		raise ValueError('More (or less) than 1 result')
	if 'Journal Article' not in ','.join([pubtype.cdata for pubtype in obj.responseWrapper.resultList.result.pubTypeList.pubType]):
		raise ValueError('Not Journal')


		
	''' build metadata dictionary'''
	metadata = {'authors' : list(), 'orcids': dict()}
	try:
		#Need to handle situation where author is listed but no full name given. For example a collective name.
		for author in obj.responseWrapper.resultList.result.authorList.author:
			try:
				metadata['authors'].append(author.fullName.cdata)
				try:
					metadata['orcids'][author.fullName.cdata] = author.authorId.cdata
				except:
					pass
			except:
				pass
		#metadata['authors'] = list([author.fullName.cdata for author in obj.responseWrapper.resultList.result.authorList.author])
		metadata['title'] = obj.responseWrapper.resultList.result.title.cdata
		metadata['date'] = obj.responseWrapper.resultList.result.firstPublicationDate.cdata
		metadata['volume'] = obj.responseWrapper.resultList.result.journalInfo.volume.cdata
		try:
			metadata['issue'] = obj.responseWrapper.resultList.result.journalInfo.issue.cdata
		except IndexError:
			pass
		metadata['pages'] = obj.responseWrapper.resultList.result.pageInfo.cdata
		metadata['journal'] = obj.responseWrapper.resultList.result.journalInfo.journal.title.cdata
		#metadata['bibcode'] = obj.responseWrapper.resultList.result.journalInfo.volume.cdata
		try:
			metadata['doi'] = obj.responseWrapper.resultList.result.DOI.cdata
		except IndexError:
			pass

		try:
			metadata['issn'] = obj.responseWrapper.resultList.result.journalInfo.journal.ISSN.cdata
		except IndexError:
			pass
		metadata['pmid'] = obj.responseWrapper.resultList.result.pmid.cdata
		try:
			metadata['pmcid'] = obj.responseWrapper.resultList.result.pmcid.cdata
		except IndexError:
			pass


		return(metadata)
	except IndexError:
		pass
