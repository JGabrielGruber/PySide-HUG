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

def addUpload(fileName):
	UploadList.addUpload(
		Upload(random.randint(0, 9999),
		fileName,
		convert_bytes(os.path.getsize(fileName)),
		0,
		""))

def sendUpload(row, manager):
	upload	= UploadList.uploads[row]
	upload['uploading']	= True
	filename			= upload['name'].split('/')[-1]

	multiPart			= QtNetwork.QHttpMultiPart(QtNetwork.QHttpMultiPart.ContentType.RelatedType)
	filedata			= QtNetwork.QHttpPart()
	filedata.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader,
		"image/jpeg")
	filedata.setHeader(QtNetwork.QNetworkRequest.ContentDispositionHeader,
		"form-data; name=media;")

	file	= QtCore.QFile(upload['name'])
	#file.ReadOnly()
	file.setParent(multiPart)
	filedata.setBodyDevice(file)
	multiPart.append(filedata)

	#multipart	= construct_multipart({ "media": filedata })
	url			= QtCore.QUrl('http://127.0.0.1:8000/medias')
	request		= QtNetwork.QNetworkRequest()
	request.setUrl(url)
	request.setRawHeader('Authorization'.encode(), ('Bearer ' + Login.token).encode())
	request.setRawHeader('FILENAME'.encode(), filename.encode())
	#upload['thread']	= QtNetwork.QNetworkAccessManager()
	print("AA")
	try:
		manager.finished.connect(finishUpload)
		rep	= manager.post(request, multiPart)
		#rep	= manager.post(request, QHttpMultiPart())
		#rep	= manager.get(request)
		manager.setParent(rep)
		#req.uploadProgress.connect(updateProgress(upload))
		print("eee")
	except Exception as e:
		print(e)

def cancelUpload(row):
	upload	= UploadList.uploads[row]
	upload['thread'].terminate()
	UploadList.uploads.pop(row)

def finishUpload():
	print("Deu boa")

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
		if upload['thread'].sent == 0:
			upload['thread'].sent	= sent
			upload['thread'].time	= time.time()
		else:
			upload['stimated']	= getTimeLeft(sent, total, upload['thread'].sent, upload['thread'].time)
		upload['thread'].response.emit()

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
