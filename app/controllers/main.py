import	random
import	os

from	models.upload	import Upload, UploadList

def addUpload(fileName):
	UploadList.addUpload(
		Upload(random.randint(0, 9999),
		fileName,
		convert_bytes(os.path.getsize(fileName)), "", ""))

def cancelUpload(row):
	UploadList.uploads.pop(row)

def startUpload(row):
	UploadList.uploads[row]['uploading']	= True

def convert_bytes(num):
	for x in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
		num /= 1024.0