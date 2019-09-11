import	sys
from	PySide2	import QtCore, QtWidgets

from	views.login	import LoginView

if __name__ == "__main__":
	app = QtWidgets.QApplication([])

	widget = LoginView()
	widget.resize(300, 200)
	widget.show()

	sys.exit(app.exec_())