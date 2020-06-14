from pathlib import Path
from os.path import join, isfile, isdir, getsize, getctime, getmtime
from os import listdir, rename
import time, json
from datetime import datetime

def is_valid_file(pth):
    try:
        p = Path(pth)
        if p.exists() and p.is_file():
            return True
    except:
        pass
    return False

def is_valid_dir(pth):
    try:
        p = Path(pth)
        if p.exists() and p.is_dir():
            return True
    except:
        pass
    return False

def get_splitted_by_pipe(s):
    l = []
    splited = str(s).split('|')
    for i in splited:
        if i != '':
            l.append(i)
    return l

def get_files(pth):
    try:
        pth = Path(pth)
        if pth.exists() and pth.is_dir():
            return [str(f) for f in listdir(pth) if isfile(join(pth, f))]
    except Exception as e:
        print('Error on getting files : ', e)
    return []

def get_folders(pth):
    try:
        pth = Path(pth)
        if pth.exists() and pth.is_dir():
            return [join(pth, f) for f in listdir(pth) if isdir(join(pth, f))]
    except Exception as e:
        print('Error on getting folders : ', e)
    return []

def get_subfolders(pth):
    all_folder = []
    folders = get_folders(pth)
    all_folder += folders
    for i in folders:
        all_folder += get_subfolders(i)
    return all_folder

def check_plural(c):
    if c > 1:
        return 's'
    return ''

def is_valid_filename(s):
    if s is not None:
        s = str(s)
        for i in ['/', '\\', '?', '"', '|', '<', '>', ':', '*']:
            if i in s:
                return False
        return True
    return False

def get_filename_extension(filename):
    if '.' not in filename:
        return filename, ''
    ext = filename.split('.')[-1]
    if '.' + ext == filename:
        return filename, ''
    return filename[:-(len('.'+ext))], ext

def get_all_files(folders):
    l = []
    for i in folders:
        l += get_files(i)
    return l

def get_int(i):
    for a in str(i):
        if a not in ['-','1','2','3','4','5','6','7','8','9','0']:
            return None
    try:
        return int(i)
    except:
        return None

class FileData:
    def __init__(self):
        self.reset()

    def reset(self):
        self.selected_folders = []

    def get_all_folders(self, include_subfolder):
        if not include_subfolder:
            return self.selected_folders
        a = []
        for i in self.selected_folders:
            a.append(i)
            a += get_subfolders(i)
        return a

    def select_dirs(self, folders):
        for folder in folders:
            folder = str(Path(folder))
            if folder not in self.selected_folders:
                self.selected_folders.append(folder)

    def get_status_txt(self):
        c = len(self.selected_folders)
        if c == 0:
            return "<big>No <b>Folder</b> is selected</big><br>Drag your folders here"
        else:
            return f"<b>{c} Folder{check_plural(c)}</b> are selected"
