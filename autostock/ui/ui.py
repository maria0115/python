import sys
from kiwoom.kiwoom import *
from PyQt5.QtWidgets import *

class UI_class():
    def __init__(self):
        print("ucclass입니다")
        self.app= QApplication(sys.argv)
        self.kiwoom = Kiwoom()
        self.app.exec_()