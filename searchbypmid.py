import requests, untangle

pmcid = 'PMC3834665'
epmc_basequeryurl = "http://www.ebi.ac.uk/europepmc/webservices/rest/search"

''' Make query to EuropePMC'''
query = {'query':pmcid,'resulttype':'core'}
r = requests.get(epmc_basequeryurl, params=query)

'''Use untangle to make python structure from xml'''
obj = untangle.parse(r.text)

print(obj.responseWrapper.hitCount.cdata)
'''test the it is ok result i.e. only one result and that is a journal article'''
if not obj.responseWrapper.hitCount.cdata == '1':
	raise ValueError('More (or less) than 1 result')
if 'Journal Article' not in ','.join([pubtype.cdata for pubtype in obj.responseWrapper.resultList.result.pubTypeList.pubType]):
	raise ValueError('Not Journal')


	
''' build metadata dictionary'''
metadata = {}
metadata['authors'] = list([author.fullName.cdata for author in obj.responseWrapper.resultList.result.authorList.author])
metadata['title'] = obj.responseWrapper.resultList.result.title.cdata
metadata['date'] = obj.responseWrapper.resultList.result.firstPublicationDate.cdata
metadata['volume'] = obj.responseWrapper.resultList.result.journalInfo.volume.cdata
metadata['issue'] = obj.responseWrapper.resultList.result.journalInfo.issue.cdata
metadata['pages'] = obj.responseWrapper.resultList.result.pageInfo.cdata
#metadata['bibcode'] = obj.responseWrapper.resultList.result.journalInfo.volume.cdata

metadata['doi'] = obj.responseWrapper.resultList.result.DOI.cdata
metadata['issn'] = obj.responseWrapper.resultList.result.journalInfo.journal.ISSN.cdata
metadata['pmid'] = obj.responseWrapper.resultList.result.pmid.cdata
metadata['pmcid'] = obj.responseWrapper.resultList.result.pmcid.cdata

print(metadata)