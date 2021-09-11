# This Python file uses the following encoding: utf-8

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit
from PyQt5 import uic

class UI(QMainWindow):
    def init(self):
        super(UI, self).init()
        uic.loadUi("window.ui", self)
        self.show()
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
