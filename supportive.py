import os
from enum import Enum
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLineEdit, QLabel, QMenu, QMainWindow, QPushButton, QVBoxLayout, QFormLayout, \
    QWidget, QProgressBar


class Act(Enum):
    copy = 1
    move = 2
    rename = 3
    change = 4
    yandex = 5
    duplicate = 6
    none = 7


class Thread(QtCore.QThread):
    signal_err = QtCore.pyqtSignal(str)
    signal_finish = QtCore.pyqtSlot()
    signal_progressbar = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread_state = Act.none
        self.from_dir: str = ""
        self.to_dir: str = ""

    def run(self):
        match self.thread_state:
            case Act.copy:
                try:
                    fresh.copy_mixed(self.from_dir, self.to_dir, self.signal_progressbar)
                    # self.signal_finish.emit()
                    pass
                except Exception as e:
                    self.signal_err.emit(str(e))
            case Act.none:
                print("None")


class MyLineEdit(QLineEdit):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parent = kwargs["parent"]

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        self.logic_line_edit(a0)

    def logic_line_edit(self, a0):
        global path_from, path_to
        if a0.key() == Qt.Key.Key_Return:
            text = self.text()
            self.clear()
            match state:
                case Act.none:
                    return
                case Act.copy:
                    if not os.path.exists(text):
                        label_set_text(self.parent.label_message, mess[3])
                        self.clear()
                        return
                    text = os.path.abspath(text)
                    if not path_from:
                        path_from = text
                        label_set_text(self.parent.label_path_from, text)
                        label_set_text(self.parent.label_message, mess[1])
                    else:
                        path_to = text
                        label_set_text(self.parent.label_path_to, text)
                        clear_labels(self.parent.label_message)
                case Act.move:
                    if not os.path.exists(text):
                        label_set_text(self.parent.label_message, mess[3])
                        self.clear()
                        return
                    text = os.path.abspath(text)
                    if not path_from:
                        path_from = text
                        label_set_text(self.parent.label_path_from, text)
                        label_set_text(self.parent.label_message, mess[2])
                    else:
                        path_to = text
                        label_set_text(self.parent.label_path_to, text)
                        clear_labels(self.parent.label_message)
                case Act.rename:
                    if not os.path.exists(text):
                        label_set_text(self.parent.label_message, mess[3])
                        self.clear()
                        return
                    text = os.path.abspath(text)
                    path_from = text
                    label_set_text(self.parent.label_path_from, text)
                    clear_labels(self.parent.label_message)
                case Act.change:
                    if not os.path.exists(text):
                        label_set_text(self.parent.label_message, mess[3])
                        self.clear()
                        return
                    text = os.path.abspath(text)
                    path_from = text
                    label_set_text(self.parent.label_path_from, text)
                    clear_labels(self.parent.label_message)
                case Act.yandex:
                    if not os.path.exists(text):
                        label_set_text(self.parent.label_message, mess[3])
                        self.clear()
                        return
                    text = os.path.abspath(text)
                    path_to = text
                    label_set_text(self.parent.label_path_from, text)
                    clear_labels(self.parent.label_message)
                case Act.duplicate:
                    if not os.path.exists(text):
                        label_set_text(self.parent.label_message, mess[3])
                        self.clear()
                        return
                    text = os.path.abspath(text)
                    path_from = text
                    label_set_text(self.parent.label_path_from, text)
                    clear_labels(self.parent.label_message)



def progress_value(length: int, max_value_progress_bar=100):
    n = 1
    percent = length / max_value_progress_bar
    temp_value = 1

    def proces():
        nonlocal n, temp_value
        value = round(n / percent)
        is_change_value = False
        n += 1
        if temp_value < value <= max_value_progress_bar:
            temp_value = value
            is_change_value = True
        return is_change_value, value

    return proces