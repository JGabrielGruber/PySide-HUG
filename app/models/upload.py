class Upload():
	id			= ""
	name		= ""
	size		= ""
	progress	= ""
	stimated	= ""

	def __init__(self, id, name, size, progress, stimated):
		self.id			= id
		self.name		= name
		self.size		= size
		self.progress	= progress
		self.stimated	= stimated

class UploadList():
	uploads	= []

	@classmethod
	def addUpload(cls, upload: Upload):
		cls.uploads.append(upload.__dict__)
