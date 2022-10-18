# This Python file uses the following encoding: utf-8
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtQuick
from PySide6 import QtGui


class Device(QtWidgets.QLabel):
    def __init__(self, parent, x, y, pixmap):
        super().__init__(parent)
#        self.frame = QtWidgets.QFrame(parent)
        self.setMinimumSize(80, 80)
#        self.label = QtWidgets.QLabel(parent)
        self.setPixmap(pixmap)
#        self.setFrameShape(QtWidgets.QFrame.Panel)
        self.setLineWidth(3)
        self.move(x,y)
#        self.frame.move(x,y)
#        self.label.move(x,y)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#        self.label.setStyleSheet("background-color: transparent;")
#        self.frame.setStyleSheet('border-color: black;')
