import os
import tempfile
import shutil
from enum import Enum
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLineEdit, QLabel, QMenu, QMainWindow, QPushButton, QVBoxLayout, QFormLayout, \
    QWidget, QProgressBar
from qt_material import apply_stylesheet

import fresh, delete_dublicates, yandex_copy
from fresh import copy_mixed
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

extra = {

    # Label colors
    'danger': '#dc3545',
    'warning': '#ffc107',
    'success': '#17a2b8',

    # Font
    'font_family': 'Roboto',
}


class Act(Enum):
    copy = 1
    move = 2
    rename = 3
    change = 4
    yandex = 5
    duplicate = 6
    none = 7


i = 1
mess = ("Укажите путь к папке с аудиофайлами:", "Укажите путь к месту куда нужно скопировать  аудиофайлы:"
        , "Укажите путь к месту куда нужно переместить  аудиофайлы:", "Такого пути не существует, укажите другой путь",
        "все действия выполнены успешно")
path_from: str = r"D:\music\path_from"

path_to: str = r"D:\music\path_to"

state = Act.none


class Thread(QtCore.QThread):
    signal_err = QtCore.pyqtSignal(str)
    signal_progressbar_set_value = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread_state = Act.none
        self.from_dir: str = ""
        self.to_dir: str = ""

    def run(self):
        match self.thread_state:
            case Act.copy:
                try:
                    fresh.copy_mixed(self.from_dir, self.to_dir, self.signal_progressbar_set_value)
                except PermissionError as p:
                    self.signal_err.emit("ошибка доступа файла")
                    logging.error(str(p), exc_info=True)
                except FileNotFoundError as f:
                    self.signal_err.emit("файл не найден")
                    logging.error(str(f), exc_info=True)
                except Exception as e:
                    self.signal_err.emit("что-то пошло не так...")
                    logging.error(str(e), exc_info=True)
            case Act.move:
                try:
                    fresh.move(self.from_dir, self.to_dir, self.signal_progressbar_set_value)
                except PermissionError as p:
                    self.signal_err.emit("ошибка доступа файла")
                    logging.error(str(p), exc_info=True)
                except FileNotFoundError as f:
                    self.signal_err.emit("файл не найден")
                    logging.error(str(f), exc_info=True)
                except Exception as e:
                    self.signal_err.emit("что-то пошло не так...")
                    logging.error(str(e), exc_info=True)
            case Act.rename:
                try:
                    fresh.rename(self.from_dir)
                except PermissionError as p:
                    self.signal_err.emit("ошибка доступа файла")
                    logging.error(str(p), exc_info=True)
                except FileNotFoundError as f:
                    self.signal_err.emit("файл не найден")
                    logging.error(str(f), exc_info=True)
                except Exception as e:
                    self.signal_err.emit("что-то пошло не так...")
                    logging.error(str(e), exc_info=True)
            case Act.change:
                temp_dir_to = tempfile.mkdtemp()
                try:
                    fresh.change(self.from_dir, temp_dir_to)
                except PermissionError as p:
                    self.signal_err.emit("ошибка доступа файла")
                    logging.error(str(p), exc_info=True)
                except FileNotFoundError as f:
                    self.signal_err.emit("файл не найден")
                    logging.error(str(f), exc_info=True)
                except Exception as e:
                    self.signal_err.emit("что-то пошло не так...")
                    logging.error(str(e), exc_info=True)
                finally:
                    shutil.rmtree(temp_dir_to)
            case Act.yandex:
                try:
                    yandex_copy.path_folder_out = self.to_dir
                    yandex_copy.copy_files()
                except PermissionError as p:
                    self.signal_err.emit("ошибка доступа файла")
                    logging.error(str(p), exc_info=True)
                except FileNotFoundError as f:
                    self.signal_err.emit("файл не найден")
                    logging.error(str(f), exc_info=True)
                except Exception as e:
                    self.signal_err.emit("что-то пошло не так...")
                    logging.error(str(e), exc_info=True)
            case Act.duplicate:
                try:
                    delete_dublicates.path_directory = self.from_dir
                    delete_dublicates.remove()
                except PermissionError as p:
                    self.signal_err.emit("ошибка доступа файла")
                    logging.error(str(p), exc_info=True)
                except FileNotFoundError as f:
                    self.signal_err.emit("файл не найден")
                    logging.error(str(f), exc_info=True)
                except Exception as e:
                    self.signal_err.emit("что-то пошло не так...")
                    logging.error(str(e), exc_info=True)


#


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
                    label_set_text(self.parent.label_path_to, text)
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


def clear_path():
    global path_from, path_to
    path_from = ""
    path_to = ""


def clear_labels(*args):
    for label in args:
        label.setText("")


def label_set_text(label: QLabel, text: str):
    label.setText(text)


def set_state(new_state: Act):
    global state
    state = new_state


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thread = Thread()
        self.min = 0
        self.max = 100
        self.menu = self.menuBar()
        self.file_menu = QMenu("Файлы")
        self.menu.addMenu(self.file_menu)
        self.copy_menu_action = QAction("Копирование с перемешиванием")
        self.move_menu_action = QAction("Перемещение с перемешиванием")
        self.rename_menu_action = QAction("Переименование")
        self.change_menu_action = QAction("Перемешать файлы в текущей папке")
        self.file_menu.addAction(self.copy_menu_action)
        self.file_menu.addAction(self.move_menu_action)
        self.file_menu.addAction(self.rename_menu_action)
        self.file_menu.addAction(self.change_menu_action)
        self.yandex_menu = QMenu("Яндекс")
        self.yandex_menu_action = QAction("Копирование файлов из 'Яндекс Музыка'")
        self.yandex_menu.addAction(self.yandex_menu_action)
        self.duplicate_menu = QMenu("Дубликаты")
        self.duplicate_menu_action = QAction("Удаление дубликатов")
        self.duplicate_menu.addAction(self.duplicate_menu_action)
        self.menu.addMenu(self.yandex_menu)
        self.menu.addMenu(self.duplicate_menu)
        self.copy_menu_action.triggered.connect(self.slot_copy_menu_action)
        self.move_menu_action.triggered.connect(self.slot_move_menu_action)
        self.rename_menu_action.triggered.connect(self.slot_rename_menu_action)
        self.change_menu_action.triggered.connect(self.slot_change_menu_action)
        self.yandex_menu_action.triggered.connect(self.slot_yandex_menu_action)
        self.duplicate_menu_action.triggered.connect(self.slot_duplicate_menu_action)
        self.progressbar = QProgressBar()
        self.thread.signal_err.connect(lambda err: self.display_err(err))
        self.thread.signal_progressbar_set_value.connect(lambda value: self.progressbar.setValue(value))
        self.thread.started.connect(self.thread_start)
        self.thread.finished.connect(self.thread_finish)

        self.widget_center = QWidget()
        self.setWindowTitle("Менеджер")
        self.label_message = QLabel()
        self.label_path_from = QLabel()
        self.line_edit = MyLineEdit(parent=self)
        # self.line_edit.
        # self.line_edit.
        self.label_path_to = QLabel()
        self.progressbar = QProgressBar()
        self.progressbar.setOrientation(Qt.Orientation.Horizontal)
        self.button_start = QPushButton("пуск")
        self.button_start.clicked.connect(self.button_clicked)
        self.label_error = QLabel()
        self.label_error.setProperty('class', 'danger')
        self.v_layout_box = QVBoxLayout()
        self.form_layout_from = QFormLayout()
        self.form_layout_to = QFormLayout()
        self.form_layout_from.addRow("Из:", self.label_path_from)
        self.form_layout_to.addRow("В:", self.label_path_to)
        self.v_layout_box.addWidget(self.label_message)
        self.v_layout_box.addLayout(self.form_layout_from)
        self.v_layout_box.addWidget(self.line_edit)
        self.v_layout_box.addLayout(self.form_layout_to)
        self.v_layout_box.addWidget(self.progressbar)
        self.v_layout_box.addWidget(self.button_start, stretch=0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.v_layout_box.addWidget(self.label_error)
        self.widget_center.setLayout(self.v_layout_box)
        self.resize(450, 300)
        self.setCentralWidget(self.widget_center)

    @QtCore.pyqtSlot()
    def slot_copy_menu_action(self):
        clear_path()
        clear_labels(self.label_message, self.label_path_to, self.label_path_from, self.label_error)
        self.label_message.setText(mess[0])
        set_state(Act.copy)

    @QtCore.pyqtSlot()
    def slot_move_menu_action(self):
        clear_path()
        clear_labels(self.label_message, self.label_path_to, self.label_path_from, self.label_error)
        self.label_message.setText(mess[0])
        set_state(Act.move)

    @QtCore.pyqtSlot()
    def slot_rename_menu_action(self):
        clear_path()
        clear_labels(self.label_message, self.label_path_to, self.label_path_from, self.label_error)
        self.label_message.setText(mess[0])
        set_state(Act.rename)

    @QtCore.pyqtSlot()
    def slot_change_menu_action(self):
        clear_path()
        clear_labels(self.label_message, self.label_path_to, self.label_path_from, self.label_error)
        self.label_message.setText(mess[0])
        set_state(Act.change)

    @QtCore.pyqtSlot()
    def slot_yandex_menu_action(self):
        clear_path()
        clear_labels(self.label_message, self.label_path_to, self.label_path_from, self.label_error)
        self.label_message.setText(mess[1])
        set_state(Act.yandex)

    @QtCore.pyqtSlot()
    def slot_duplicate_menu_action(self):
        clear_path()
        clear_labels(self.label_message, self.label_path_to, self.label_path_from, self.label_error)
        self.label_message.setText(mess[0])
        set_state(Act.duplicate)

    @QtCore.pyqtSlot()
    def display_err(self, err):
        self.label_error.setText(err)

    @QtCore.pyqtSlot()
    def button_clicked(self):
        if state == Act.none:
            return
        self.thread.from_dir = path_from
        self.thread.to_dir = path_to
        self.thread.thread_state = state
        self.thread.start()

    def thread_finish(self):
        self.progressbar.reset()
        label_set_text(self.label_message, mess[4])
        if state == Act.change or Act.yandex:
            self.progressbar.setMinimum(self.min)
            self.progressbar.setMaximum(self.max)

    def thread_start(self):
        if state == Act.change or state == Act.yandex:
            self.progressbar.setMinimum(0)
            self.progressbar.setMaximum(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    apply_stylesheet(app, theme='light_blue.xml', extra=extra)
    mw.show()
    sys.exit(app.exec())
