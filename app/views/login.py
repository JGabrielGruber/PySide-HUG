import	time
from	PySide2 import QtCore, QtWidgets, QtGui

from	controllers		import login as loginController
from	models.login	import Login
from	views.main		import MainView

class LoginView(QtWidgets.QWidget):
	main	= None
	def __init__(self):
		super().__init__()

		self.button		= QtWidgets.QPushButton("Login")
		self.text		= QtWidgets.QLabel("Inform your credentials \n Username: admin\n Password: senha")
		self.message	= QtWidgets.QMessageBox()
		self.username	= QtWidgets.QLineEdit("")
		self.password	= QtWidgets.QLineEdit("")
		self.text.setAlignment(QtCore.Qt.AlignCenter)
		self.username.setPlaceholderText("Username")
		self.password.setPlaceholderText("Password")
		self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.username)
		self.layout.addWidget(self.password)
		self.layout.addWidget(self.button)
		self.setLayout(self.layout)

		self.button.clicked.connect(self.login)

	def showMain(self):
		if Login.token:
			self.main.show()

	def login(self):
		Login.setCredentials(
			self.username.text(),
			self.password.text()
		)
		resp	= loginController.getToken()
		if not resp:
			self.main	= MainView()
			self.main.resize(800, 600)
			self.main.show()
			self.hide()
		else:
			self.message.setText(resp)
			self.message.show()