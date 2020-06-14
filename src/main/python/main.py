from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui, QtWidgets, QtCore
from main_ui import Ui_MainWindow

import sys, os

app = ApplicationContext()

class MainWindow(QtWidgets.QMainWindow):
    ui = Ui_MainWindow()
    
    app_version = app.build_settings['version']
    main_icon = app.get_resource('icon.png')

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("File to Dir")
        self.ui.setupUi(self)
        self.setIcons()
    
    def setIcons(self):
        icon = QtGui.QIcon(app.get_resource('reset.png'))
        self.ui.actionReset.setIcon(icon)
        self.ui.actionReset_1.setIcon(icon)
        icon = QtGui.QIcon(app.get_resource('exit.png'))
        self.ui.actionExit.setIcon(icon)
        self.ui.actionExit_1.setIcon(icon)
        icon = QtGui.QIcon(app.get_resource('plus.png'))
        self.ui.actionAdd.setIcon(icon)
        self.ui.actionAdd_1.setIcon(icon)
        icon = QtGui.QIcon(app.get_resource('clear.png'))
        self.ui.actionClear.setIcon(icon)
        self.ui.actionClear_1.setIcon(icon)
        self.ui.actionAdd_Multiple_Folder.setIcon(QtGui.QIcon(app.get_resource('add.png')))
        self.ui.actionAbout_the_Author.setIcon(QtGui.QIcon(self.main_icon))

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
