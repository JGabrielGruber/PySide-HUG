import	random

from	models.upload	import Upload, UploadList

def addUpload(fileName):
	UploadList.addUpload(Upload(random.randint(), fileName, "", "", ""))