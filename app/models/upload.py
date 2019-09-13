class Upload():
	id			= ""
	name		= ""
	size		= ""
	progress	= ""
	estimated	= ""
	uploading	= False

	def __init__(self, id, name, size, progress, estimated, thread):
		self.id			= id
		self.name		= name
		self.size		= size
		self.progress	= progress
		self.estimated	= estimated
		self.uploading	= False
		self.thread		= thread

class UploadList():
	uploads	= []

	@classmethod
	def addUpload(cls, upload: Upload):
		cls.uploads.append(upload.__dict__)
