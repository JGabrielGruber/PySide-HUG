class Media():
	id			= ""
	filename		= ""
	timestamp	= ""

	def __init__(self, id, filename, timestamp):
		self.id			= id
		self.filename	= filename
		self.timestamp	= timestamp

class MediaList():
	medias	= []

	@classmethod
	def addMedia(cls, media: Media):
		cls.medias.append(media.__dict__)
