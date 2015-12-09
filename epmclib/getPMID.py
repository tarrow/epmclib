from . getID import getID

class getPMID(getID):
	"""Add the correct query string to only search for PMIDs"""
	def __init__(self, id):
		self.query = 'ext_id:' + id + ' src:med'
