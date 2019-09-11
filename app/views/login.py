from PySide2 import QtCore, QtWidgets, QtGui

class LoginView(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.button		= QtWidgets.QPushButton("Login")
		self.text		= QtWidgets.QLabel("Inform your credentials \n Username: admin\n Password: senha")
		self.username	= QtWidgets.QLineEdit("")
		self.username.setPlaceholderText("Username")
		self.password	= QtWidgets.QLineEdit("")
		self.password.setPlaceholderText("Password")
		self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
		self.text.setAlignment(QtCore.Qt.AlignCenter)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.username)
		self.layout.addWidget(self.password)
		self.layout.addWidget(self.button)
		self.setLayout(self.layout)

		self.button.clicked.connect(self.login)


	def login(self):
		self.text.setText("Logged!")