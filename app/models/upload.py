from	PySide2	import QtCore

class SendSignal(QtCore.QObject):
	sender = QtCore.Signal(object, int)

class Upload(QtCore.QObject):
	id			= ""
	name		= ""
	size		= ""
	progress	= ""
	estimated	= ""
	uploading	= False

	def __init__(self, id, name, size, fun):
		self.id			= id
		self.name		= name
		self.size		= size
		self.progress	= 0
		self.estimated	= ""
		self.uploading	= False
		self.manager	= None
		self.time		= ""
		self.sent		= 0
		self.reply		= None
		self.stream		= None
		self.multiPart	= None
		self.signal		= SendSignal()
		self.signal.sender.connect(fun)

class UploadList():
	uploads	= []

	@classmethod
	def addUpload(cls, upload: Upload):
		cls.uploads.append(upload.__dict__)
