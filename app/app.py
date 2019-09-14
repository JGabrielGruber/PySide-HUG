import	sys
from	PySide2	import QtCore, QtWidgets, QtGui

from	views.login	import LoginView

if __name__ == "__main__":
	app = QtWidgets.QApplication([])	
	app.setQuitOnLastWindowClosed(False)

	widget = LoginView()
	widget.resize(300, 200)
	widget.show()

	icon	= QtGui.QIcon("icon.png")

	app.setWindowIcon(icon)

	tray = QtWidgets.QSystemTrayIcon(icon, app)
	tray.setVisible(True)

	def showApp():
		widget.showMain()

	def exitApp():
		app.exit()

	menu = QtWidgets.QMenu()
	show = QtWidgets.QAction("Open App")
	show.triggered.connect(showApp)
	exit = QtWidgets.QAction("Exit App")
	exit.triggered.connect(exitApp)
	menu.addAction(show)
	menu.addSeparator()
	menu.addAction(exit)

	tray.setContextMenu(menu)
	tray.setToolTip("PySide&HUG")
	tray.show()

	sys.exit(app.exec_())