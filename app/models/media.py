class Media():
	id			= ""
	name		= ""
	timestamp	= ""

	def __init__(self, id, name, timestamp):
		self.id			= id
		self.name		= name
		self.timestamp	= timestamp

class MediaList():
	medias	= []

	@classmethod
	def addMedia(cls, media: Media):
		cls.medias.append(media.__dict__)
