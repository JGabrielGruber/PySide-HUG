from	PySide2 import QtCore, QtWidgets, QtGui

from	controllers		import main
from	models.upload	import  UploadList, Upload

class MainView(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.text_medias	= QtWidgets.QLabel("Files list:")
		self.text_upload	= QtWidgets.QLabel("Upload list:")
		self.text_medias.setAlignment(QtCore.Qt.AlignCenter)

		self.container	= QtWidgets.QVBoxLayout()

		self.titles	= QtWidgets.QHBoxLayout()
		self.titles.addWidget(self.text_medias, 1, QtCore.Qt.AlignLeft)
		self.titles.addWidget(self.text_upload, 2)
		self.container.addLayout(self.titles)

		self.list_medias	= QtWidgets.QListWidget()
		self.list_medias.addItems(['aaa', 'bbb'])

		self.table_upload	= QtWidgets.QTableWidget()
		self.table_upload.setColumnCount(5)
		self.table_upload.setHorizontalHeaderLabels(['Name', 'Size', 'Progress', 'Stimated', 'Cancel'])
		self.table_upload.setModel()

		self.lists	= QtWidgets.QHBoxLayout()
		self.lists.addWidget(self.list_medias, 1, QtCore.Qt.AlignLeft)

		self.upload	= QtWidgets.QVBoxLayout()
		self.upload.addWidget(self.table_upload)

		self.button_find	= QtWidgets.QPushButton("Search File")
		self.button_upload	= QtWidgets.QPushButton("Upload File")
		self.button_find.clicked.connect(self.findFile)

		self.buttons	= QtWidgets.QHBoxLayout()
		self.buttons.addWidget(self.button_find)
		self.buttons.addWidget(self.button_upload)

		self.upload.addLayout(self.buttons)

		self.lists.addLayout(self.upload, 2)
		self.container.addLayout(self.lists)
		self.setLayout(self.container)
	
	def findFile(self):
		fileName,	= QtWidgets.QFileDialog.getOpenFileName()
		main.addUpload(fileName)