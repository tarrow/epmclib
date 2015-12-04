from . getID import getID

class getPMCID(getID):
	def __init__(self, id):
		if id[:3] != "PMC":
			id = 'PMC' + id
		self.query = 'PMCID:' + id
