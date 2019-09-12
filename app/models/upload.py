class Upload():
	id			= ""
	name		= ""
	size		= ""
	progress	= ""
	estimated	= ""
	uploading	= False

	def __init__(self, id, name, size, progress, estimated):
		self.id			= id
		self.name		= name
		self.size		= size
		self.progress	= progress
		self.estimated	= estimated
		self.uploading	= False

class UploadList():
	uploads	= []

	@classmethod
	def addUpload(cls, upload: Upload):
		cls.uploads.append(upload.__dict__)
