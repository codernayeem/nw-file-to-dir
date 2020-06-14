from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui, QtWidgets, QtCore
from main_ui import Ui_MainWindow
from tools import FileData, join, Path, is_valid_dir

import sys, os

app = ApplicationContext()

class MainWindow(QtWidgets.QMainWindow):
    ui = Ui_MainWindow()
    FILEDATA = FileData()

    app_version = app.build_settings['version']
    main_icon = app.get_resource('icon.png')
    last_selected_dir = 'C:'

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
        self.ui.actionAdd_1.triggered.connect(self.select_folder)
        self.ui.actionAdd_Multiple_Folder.triggered.connect(lambda: self.select_folder(multiple=True))
        self.ui.actionClear.triggered.connect(self.clear_all_folders)
        # self.ui.actionReset.triggered.connect(self.reset_all)

        # toolbar
        self.ui.actionAdd.triggered.connect(self.select_folder)
        self.ui.actionClear.triggered.connect(self.clear_all_folders)
        # self.ui.actionReset.triggered.connect(self.reset_all)
        self.ui.actionExit.triggered.connect(sys.exit)

        # button
        # self.ui.output_bt.clicked.connect(self.select_output_folder)
        # self.ui.bt_go.clicked.connect(self.go_for_work)

    def select_folder(self, multiple=False, drag=False, folders=None):
        if multiple:
            file_dialog = QtWidgets.QFileDialog(directory=self.last_selected_dir)
            file_dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
            file_dialog.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
            file_dialog.setWindowTitle("Select Folders")
            file_dialog.setWindowIcon(QtGui.QIcon(self.main_icon))
            f_tree_view = file_dialog.findChild(QtWidgets.QTreeView)
            if f_tree_view:
                f_tree_view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
            if not file_dialog.exec():
                return
            folders = file_dialog.selectedFiles()
        elif drag:
            folders = [f for f in folders if is_valid_dir(f)]
        else:
            folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory=self.last_selected_dir))
            if folder == '':
                return
            folder = str(Path(folder))
            self.last_selected_dir = join(*folder.split('\\')[:len(folder.split('\\'))-1])
            folders = [folder]
        self.FILEDATA.select_dirs(folders)
        self.ui.txt_stat.setText(self.FILEDATA.get_status_txt())

    def clear_all_folders(self):
        self.FILEDATA.reset()
        self.ui.txt_stat.setText(self.FILEDATA.get_status_txt())


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
