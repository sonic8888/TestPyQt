import os
from enum import Enum
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QLineEdit, QLabel, QMenu, QMainWindow, QPushButton, QVBoxLayout, QFormLayout, \
    QWidget, QProgressBar






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