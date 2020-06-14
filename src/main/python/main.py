from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtGui, QtWidgets, QtCore
from main_ui import Ui_MainWindow
from dialogs import Ui_AboutPage
from tools import FileData, is_valid_dir, join, Path, get_filename_extension, get_files
from shutil import copyfile, move

import sys, os

app = ApplicationContext()


class CustomLabel(QtWidgets.QLabel):
    def __init__(self, parent, main):
        super(QtWidgets.QLabel, self).__init__(parent)
        self.setAcceptDrops(True)
        self.Root = main
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.Root.select_folder(drag=True, folders=[i.toLocalFile() for i in event.mimeData().urls()])


class MainWindow(QtWidgets.QMainWindow):
    ui = Ui_MainWindow()
    FILEDATA = FileData()
    about_page = None

    app_version = app.build_settings['version']
    main_icon = app.get_resource('icon.png')

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("File to Dir")
        self.ui.setupUi(self, CustomLabel)
        self.setIcons()
        self.set_menu_toolbar_button_action()
        self.reset_all()
    
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
        self.ui.actionAbout_the_Author.triggered.connect(self.see_about)
        self.ui.actionExit_1.triggered.connect(lambda: sys.exit(0))
        self.ui.actionAdd_1.triggered.connect(self.select_folder)
        self.ui.actionAdd_Multiple_Folder.triggered.connect(lambda: self.select_folder(multiple=True))
        self.ui.actionClear.triggered.connect(self.clear_all_folders)
        self.ui.actionReset.triggered.connect(self.reset_all)

        # toolbar
        self.ui.actionAdd.triggered.connect(self.select_folder)
        self.ui.actionClear.triggered.connect(self.clear_all_folders)
        self.ui.actionReset.triggered.connect(self.reset_all)
        self.ui.actionExit.triggered.connect(sys.exit)

        # button
        self.ui.output_bt.clicked.connect(self.select_output_folder)
        self.ui.bt_go.clicked.connect(self.go_for_work)

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

    def select_output_folder(self):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Output Directory", directory=self.last_selected_out_dir))
        if folder != '':
            folder = str(Path(folder))
            self.last_selected_out_dir = join(*folder.split('\\')[:len(folder.split('\\'))-1])
            self.ui.input_2.setText(folder)

    def reset_all(self):
        self.last_selected_dir = 'C:'
        self.last_selected_out_dir = 'C:'
        self.ui.side_input_2.setChecked(False)
        self.ui.side_input_3.setChecked(False)
        self.ui.side_input_4.setText('')
        self.ui.side_input_5.setText('')
        self.ui.side_input_6.setText('')
        self.ui.side_input_7.setText('')
        self.ui.side_input_8.setChecked(False)
        self.ui.side_input_9.setChecked(False)
        self.ui.side_input_10.setText('')
        self.ui.side_input_11.setText('')
        self.ui.side_input_12.setText('')
        self.ui.side_input_13.setText('')
        self.ui.input_1.setCurrentIndex(0)
        self.ui.input_2.setText('')
        self.clear_all_folders()

    def see_about(self):
        if self.about_page is None:
            self.about_page = QtWidgets.QWidget()
            self.about_page.ui = Ui_AboutPage()
            self.about_page.ui.setupUi(self.about_page)
            self.about_page.ui.version.setText(f'v{self.app_version}')
            self.about_page.ui.icon.setPixmap(QtGui.QPixmap(self.main_icon))
            self.about_page.ui.name.setText("File To Dir")
        self.about_page.destroy()
        self.about_page.show()

    def go_for_work(self):
        i1 = self.ui.input_1.currentIndex()
        i2 = self.ui.input_2.text()
        include_subfolder = self.ui.side_input_1.isChecked()
        if i2.strip() == '':
            return QtWidgets.QMessageBox.warning(self, "Warning", f"<p style=\"font-size: 10pt;\"><b>Error Found.</b> Please, give Output Directory.</p>")
        i2 = Path(i2)
        if not (i2.exists() and i2.is_dir()):
            return QtWidgets.QMessageBox.warning(self, "Warning", f"<p style=\"font-size: 10pt;\"><b>Error Found.</b> Output Directory not exist.</p>")

        folders = self.FILEDATA.get_all_folders(include_subfolder)

        data = {
            's2': self.ui.side_input_2.isChecked(),
            's3': self.ui.side_input_3.isChecked(),
            's4': self.ui.side_input_4.text(),
            's5': self.ui.side_input_5.text(),
            's6': self.ui.side_input_6.text(),
            's7': self.ui.side_input_7.text(),
            's8': self.ui.side_input_8.isChecked(),
            's9': self.ui.side_input_9.isChecked(),
            's10': self.ui.side_input_10.text(),
            's11': self.ui.side_input_11.text(),
            's12': self.ui.side_input_12.text(),
            's13': self.ui.side_input_13.text(),
        }

        done = 0
        fail = 0
        ignored = 0
        not_allowed = 0

        for folder in folders:
            for a_file in get_files(folder):
                status = self.check_for_allow_and_ignore(a_file, data)
                if status == 1:
                    ignored += 1
                elif status == 2:
                    not_allowed += 1
                else:
                    try:
                        if i1 == 0:
                            copyfile(join(folder, a_file), join(i2, a_file))
                        else:
                            move(join(folder, a_file), join(i2, a_file))
                        done += 1
                    except:
                        fail += 1

        info = f"<p style=\"font-size: 10pt;\"><b>Finished.</b> {done} files "
        if i1 == 0:
            info += 'copied'
        else:
            info += 'moved'
        if fail:
            info += f" | {fail} files failed"
        if ignored:
            info += f" | {ignored} files ignored"
        if not_allowed:
            info += f" | {not_allowed} files not allowed"
        info += '.'
        QtWidgets.QMessageBox.warning(self, "Info", info)

    def check_for_allow_and_ignore(self, fl_name, data):
        filename, ext = get_filename_extension(fl_name)
        if data['s8']:
            if (data['s9'] and not ext) or (data['s10'] and ext in data['s10']):
                return 1
            if data['s11']:
                for i in data['s11']:
                    if filename.startswith(i):
                        return 1
            if data['s12']:
                for i in data['s12']:
                    if filename.endswith(i):
                        return 1
            if data['s13']:
                for i in data['s13']:
                    if i in filename:
                        return 1

        if data['s2']:
            add_item = False
            if (data['s3'] and not ext) or (data['s4'] and ext in data['s4']):
                add_item = True
            elif data['s5']:
                for i in data['s5']:
                    if filename.startswith(i):
                        add_item = True
                        break
            elif data['s6']:
                for i in data['s6']:
                    if filename.endswith(i):
                        add_item = True
                        break
            elif data['s7']:
                for i in data['s7']:
                    if i in filename:
                        add_item = True
                        break
            if not add_item:
                return 2
        return 0


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.app.exec_())
