from . getID import getID

class getPMCID(getID):
	def __init__(self, id):
		"""Add the correct prefix to europepmc query to only get pmcids + correct for PMCIDS not starting PMC"""
		if id[:3] != "PMC":
			id = 'PMC' + id
		self.query = 'PMCID:' + id
