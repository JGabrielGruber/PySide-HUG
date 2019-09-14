import	json
import	random
import	pycurl
import	os
import	time
from	PySide2				import QtCore, QtNetwork
from	requests_toolbelt	import MultipartEncoder, MultipartEncoderMonitor
from	io					import BytesIO, StringIO

from	models.upload	import Upload, UploadList
from	models.media	import Media, MediaList
from	models.login	import Login

def construct_multipart(files):
	multiPart = QtNetwork.QHttpMultiPart(QtNetwork.QHttpMultiPart.FormDataType)

	for key, file in files.items():
		imagePart = QtNetwork.QHttpPart()
		fileName = QtCore.QFileInfo(file.fileName()).fileName()
		imagePart.setHeader(QtNetwork.QNetworkRequest.ContentDispositionHeader,
			"form-data; name=\"%s\"; filename=\"%s\"" % (key, fileName))
		imagePart.setBodyDevice(file)
		multiPart.append(imagePart)
	return multiPart

def addUpload(fileName, fun):
	UploadList.addUpload(
		Upload(random.randint(0, 9999),
		fileName,
		convert_bytes(os.path.getsize(fileName)),
		fun))

def sendUpload(row):
	upload				= UploadList.uploads[row]
	upload['uploading']	= True
	filename			= upload['name'].split('/')[-1]
	multiPart			= QtNetwork.QHttpMultiPart(QtNetwork.QHttpMultiPart.ContentType.RelatedType)
	filedata			= QtNetwork.QHttpPart()

	file	= QtCore.QFile(upload['name'])
	file.open(QtCore.QIODevice.ReadOnly)
	file.setParent(multiPart)
	upload['stream']	= file
	filedata.setBodyDevice(file)
	multiPart.append(filedata)
	upload['multiPart']	= multiPart

	url			= QtCore.QUrl('http://127.0.0.1:8000/medias')
	request		= QtNetwork.QNetworkRequest()
	request.setUrl(url)
	request.setRawHeader('Authorization'.encode(), ('Bearer ' + Login.token).encode())
	request.setRawHeader('FILENAME'.encode(), filename.encode())
	upload['manager']	= QtNetwork.QNetworkAccessManager()
	upload['manager'].finished.connect(finishUpload(row))
	try:
		upload['reply']	= upload['manager'].post(request, upload['multiPart'])
		upload['manager'].setParent(upload['reply'])
		upload['reply'].uploadProgress.connect(updateProgress(upload))
	except Exception as e:
		print(e)

def cancelUpload(row):
	upload	= UploadList.uploads[row]
	upload['reply'].abort()
	UploadList.uploads.pop(row)

def finishUpload(row):
	upload	= UploadList.uploads[row]
	#UploadList.uploads.pop(row)
	upload['signal'].sender.emit()

def progress(function):
	def wrapper(upload):
		def updateProgress(sent, total, **kwargs):
			return function(sent, total, upload, **kwargs)
		return updateProgress
	return wrapper

@progress
def updateProgress(sent, total, upload):
	if total > 0:
		upload['progress']	= (sent / total) * 100
		if upload['sent'] == 0:
			upload['sent']	= sent
			upload['time']	= time.time()
		else:
			upload['stimated']	= getTimeLeft(sent, total, upload['sent'], upload['time'])
		upload['signal'].sender.emit()

def requestList(manager):
	url		= QtCore.QUrl('http://127.0.0.1:8000/medias')
	request	= QtNetwork.QNetworkRequest()
	request.setUrl(url)
	request.setRawHeader('Authorization'.encode(), ('Bearer ' + Login.token).encode())
	manager.get(request)

def getReply(function):
	def wrapper(fun):
		def passIt(reply, **kwargs):
			return function(reply, fun, **kwargs)
		return passIt
	return wrapper

@getReply
def getList(reply, fun):
	try:
		data	= json.loads(reply.readAll().data().decode('utf-8'))
		for item in data:
			MediaList.addMedia(Media(
				item['id'],
				item['filename'],
				item['timestamp']
			))
		fun.emit()
	except Exception as e:
		print(e)
		pass


def getTimeLeft(sent, total, old_sent, old_time):
	remain	= ((sent - total) * (old_time - time.time())) / sent
	if remain > 60:
		return '{0:.1f} min'.format(remain / 60)
	else:
		return '{0:.0f} sec'.format(remain)

def convert_bytes(num):
	for x in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
		num /= 1024.0
