from	PySide2 import QtCore, QtWidgets, QtGui


class MainView(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.text		= QtWidgets.QLabel("Here you are")
		self.text.setAlignment(QtCore.Qt.AlignCenter)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.text)
		self.setLayout(self.layout)