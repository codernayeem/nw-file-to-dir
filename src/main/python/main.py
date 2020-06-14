from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui, QtWidgets, QtCore
from main_ui import Ui_MainWindow

import sys, os

app = ApplicationContext()

class MainWindow(QtWidgets.QMainWindow):
    ui = Ui_MainWindow()
    app_version = app.build_settings['version']

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("File to Dir")
        self.ui.setupUi(self)

if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
