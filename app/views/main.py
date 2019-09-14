import	time

from	PySide2 import QtCore, QtWidgets, QtGui, QtNetwork

from	controllers		import main
from	models.upload	import UploadList, Upload
from	models.media	import MediaList, Media

class MainView(QtWidgets.QWidget):
	sig_updateList	= QtCore.Signal()

	def __init__(self):
		super().__init__()

		#self.uploader		= main.Uploader()
		#self.uploader.response.connect(self.updateTable)

		self.sig_updateList.connect(self.updateList)

		self.manager		= QtNetwork.QNetworkAccessManager()
		self.manager.finished.connect(main.getList(self.sig_updateList))

		self.text_medias	= QtWidgets.QLabel("Files list:")
		self.text_upload	= QtWidgets.QLabel("Upload list:")
		self.text_medias.setAlignment(QtCore.Qt.AlignCenter)

		self.container	= QtWidgets.QVBoxLayout()

		self.titles	= QtWidgets.QHBoxLayout()
		self.titles.addWidget(self.text_medias, 1, QtCore.Qt.AlignLeft)
		self.titles.addWidget(self.text_upload, 2)
		self.container.addLayout(self.titles)

		self.list_medias	= QtWidgets.QListWidget()

		self.table_upload	= QtWidgets.QTableWidget()
		self.table_upload.setColumnCount(5)
		self.table_upload.setHorizontalHeaderLabels(['Name', 'Size', 'Progress', 'Estimated', 'Option'])

		self.lists	= QtWidgets.QHBoxLayout()
		self.lists.addWidget(self.list_medias, 1, QtCore.Qt.AlignLeft)

		self.upload	= QtWidgets.QVBoxLayout()
		self.upload.addWidget(self.table_upload)

		self.button_find	= QtWidgets.QPushButton("Search File")
		self.button_find.clicked.connect(self.findFile)

		self.upload.addWidget(self.button_find)

		self.lists.addLayout(self.upload, 2)
		self.container.addLayout(self.lists)
		self.setLayout(self.container)

		main.requestList(self.manager)
		self.updateTable()
	
	def findFile(self):
		fileName	= QtWidgets.QFileDialog.getOpenFileName()
		if fileName[0] != "":
			main.addUpload(fileName[0], self.updateTable)
			self.updateTable()
	
	def updateTable(self):
		if UploadList.uploads:
			for row, upload in enumerate(UploadList.uploads):
				self.table_upload.setRowCount(row + 1)
				self.table_upload.setItem(row, 0, QtWidgets.QTableWidgetItem(upload['name']))
				self.table_upload.setItem(row, 1, QtWidgets.QTableWidgetItem(str(upload['size'])))
				progressBar	= QtWidgets.QProgressBar()
				progressBar.setValue(upload['progress'])
				self.table_upload.setCellWidget(row, 2, progressBar)
				self.table_upload.setItem(row, 3, QtWidgets.QTableWidgetItem(upload['estimated']))
				if upload['uploading']:
					self.buttonn_cancel	= QtWidgets.QPushButton('Cancel')
					self.buttonn_cancel.clicked.connect(self.handleCancel)
					self.table_upload.setCellWidget(row, 4, self.buttonn_cancel)
				else:
					self.buttonn_send	= QtWidgets.QPushButton('Send')
					self.buttonn_send.clicked.connect(self.handleSend)
					self.table_upload.setCellWidget(row, 4, self.buttonn_send)
		else:
			self.table_upload.setRowCount(0)

	def handleCancel(self):
		button	= QtGui.qApp.focusWidget()
		index	= self.table_upload.indexAt(button.pos())
		if index.isValid():
			main.cancelUpload(index.row())
			self.updateTable()
	
	def handleSend(self):
		button		= QtGui.qApp.focusWidget()
		index		= self.table_upload.indexAt(button.pos())
		if index.isValid():
			main.sendUpload(index.row())

	def updateList(self):
		if MediaList.medias:
			for media in MediaList.medias:
				self.list_medias.addItem(media['filename'] + " - " + media['timestamp'])
