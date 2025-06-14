#!/usr/bin/env python3

from PyQt5 import QtCore
from view import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os


QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class Controller(QMainWindow, Ui_MainWindow):    
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setUpActions()

        self.show()

    def setUpActions(self):
        pass


    