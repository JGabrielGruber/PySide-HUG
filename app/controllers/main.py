import	json
import	random
import	pycurl
import	os
import	time
from	PySide2				import QtCore, QtNetwork
from	requests_toolbelt	import MultipartEncoder, MultipartEncoderMonitor
from	io					import BytesIO, StringIO

from	models.upload	import Upload, UploadList
from	models.login	import Login

class Uploader(QtCore.QThread):
	response	= QtCore.Signal()

	def __init__(self, row):
		QtCore.QThread.__init__(self)
		self.row	= row

	def run(self):
		upload				= UploadList.uploads[self.row]
		upload['uploading']	= True
		self.response.emit()
		filename			= upload['name'].split('/')[-1]
		filedata			= QtCore.QFile(upload['name'])
		filedata.open(QtCore.QFile.ReadOnly)
		multipart	= construct_multipart({ "media": filedata })
		url			= QtCore.QUrl('http://127.0.0.1:8000/medias')
		request		= QtNetwork.QNetworkRequest()
		request.setUrl(url)
		request.setRawHeader('Authorization'.encode(), ('Bearer ' + Login.token).encode())
		request.setRawHeader('FILENAME'.encode(), filename.encode())
		request.setHeader(
			QtNetwork.QNetworkRequest.ContentTypeHeader,
			'multipart/form-data; boundary=%s' % multipart.boundary
		)
		manager	= QtNetwork.QNetworkAccessManager()
		manager.finished.connect(finished)
		req	= manager.post(request, multipart)
		req.uploadProgress.connect(updateProgress(upload))

def update(total):
	print(total)

def finished(reply):
	print("Finished: ", reply.readAll())

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

def send(row):
	upload	= UploadList.uploads[row]
	upload['uploading']	= True
	with open(upload['name'], 'rb') as f:
		filename	= upload['name'].split('/')[-1]
		curl		= pycurl.Curl()
		curl.setopt(curl.POST, 1)
		curl.setopt(curl.NOPROGRESS, 0)
		#curl.setopt(curl.PROGRESSFUNCTION, updateProgress(upload))
		curl.setopt(curl.HTTPPOST, [('title', 'test'), (('media', (curl.FORM_FILE, upload['name'])))])
		curl.setopt(curl.HTTPHEADER, [
			'Authorization: Bearer ' + Login.token,
			'FILENAME: ' + filename
		])
		curl.setopt(curl.VERBOSE, 1)
		bodyOutput		= BytesIO()
		headersOutput	= StringIO()
		curl.setopt(curl.WRITEFUNCTION, bodyOutput.write)
		curl.setopt(curl.URL, 'http://127.0.0.1:8000/medias')
		curl.setopt(curl.WRITEFUNCTION, headersOutput.write)
		curl.perform()
		#print(bodyOutput.getvalue)

def addUpload(fileName):
	UploadList.addUpload(
		Upload(random.randint(0, 9999),
		fileName,
		convert_bytes(os.path.getsize(fileName)),
		0,
		"",
		Uploader(0)))

def sendUpload(row, fun):
	upload	= UploadList.uploads[row]
	upload['thread'].row	= row
	upload['thread'].response.connect(fun)
	upload['thread'].start()

def cancelUpload(row):
	upload	= UploadList.uploads[row]
	upload['thread'].terminate()
	UploadList.uploads.pop(row)

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
		upload['thread'].response.emit()

def convert_bytes(num):
	for x in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
		num /= 1024.0
