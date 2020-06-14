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
        self.set_menu_toolbar_button_action()
    
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


    def set_menu_toolbar_button_action(self):
        # menu
        # self.ui.actionAbout_the_Author.triggered.connect(self.see_about)
        self.ui.actionExit_1.triggered.connect(lambda: sys.exit(0))
        # self.ui.actionAdd_1.triggered.connect(self.select_folder)
        # self.ui.actionAdd_Multiple_Folder.triggered.connect(lambda: self.select_folder(multiple=True))
        # self.ui.actionClear.triggered.connect(self.clear_all_folders)
        # self.ui.actionReset.triggered.connect(self.reset_all)

        # toolbar
        # self.ui.actionAdd.triggered.connect(self.select_folder)
        # self.ui.actionClear.triggered.connect(self.clear_all_folders)
        # self.ui.actionReset.triggered.connect(self.reset_all)
        self.ui.actionExit.triggered.connect(sys.exit)

        # button
        # self.ui.output_bt.clicked.connect(self.select_output_folder)
        # self.ui.bt_go.clicked.connect(self.go_for_work)


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
