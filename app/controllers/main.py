import	random
import	requests
import	os
import	time
from	PySide2				import QtCore
from	requests_toolbelt	import MultipartEncoder, MultipartEncoderMonitor
from	threading			import Thread

from	models.upload	import Upload, UploadList
from	models.login	import Login

class Uploader(QtCore.QThread):
	response	= QtCore.Signal(int)

	def __init__(self, row, parent=None):
		super(Uploader, self).__init__(parent)
		self.row	= row

	def run(self):
		upload	= UploadList.uploads[self.row]
		upload['uploading']	= True
		with open(upload['name'], 'rb') as f:
			filename	= upload['name'].split('/')[-1]
			encoder		= MultipartEncoder({ 'media' : ( upload['name'], f, 'application/octet-stream', { "Content-Transfer-Encoding": "binary" }) })
			callback	= create_callback(encoder, upload)
			monitor		= MultipartEncoderMonitor(encoder, callback)
			r	= requests.post(
				'http://localhost:8000/medias',
				headers={
					'Authorization': 'Bearer ' +  Login.token,
					'FILENAME': filename,
					'Content-Type': monitor.content_type
				},
				data=monitor
			)
		#self.emit(QtCore.Signal('STATUS'), UploadList.uploads.pop(self.row))

def addUpload(fileName):
	UploadList.addUpload(
		Upload(random.randint(0, 9999),
		fileName,
		convert_bytes(os.path.getsize(fileName)),
		0,
		""))

def cancelUpload(row):
	UploadList.uploads.pop(row)

def convert_bytes(num):
	for x in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
		num /= 1024.0

def create_callback(encoder, upload):
	encoder_len = encoder.len

	def callback(monitor):
		upload['progress']	= (monitor.bytes_read / encoder_len) * 100
		print(upload['progress'])
	return callback
